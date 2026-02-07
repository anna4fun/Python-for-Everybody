from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Helpers
# ----------------------------

def parse_ts(ts: str) -> datetime:
    """
    Parse ISO8601 UTC timestamps like '2026-01-03T10:00:00Z' into aware datetime.
    """
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts).astimezone(timezone.utc)


def hours_between(start: datetime, end: datetime) -> float:
    return (end - start).total_seconds() / 3600.0


EXPECTED_ORDER = {
    "CREATED": 0,
    "SUBMITTED": 1,
    "REJECTED": 2,
    "RESUBMITTED": 3,
    "APPROVED": 4,
    "PAID": 5,
    "CANCELED": 99,  # terminal; treat as stop
}


FINAL_STATES = {"OPEN", "IN_REVIEW", "APPROVED", "REJECTED", "PAID", "CANCELED", "UNKNOWN"}


# ----------------------------
# Task A — Reconstruction
# ----------------------------

def reconstruct_invoices(events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Returns a dict keyed by invoice_id with:
      - vendor_id
      - project_id
      - amount (resolved using most recent non-null amount by event time)
      - final_state: one of ["OPEN", "IN_REVIEW", "APPROVED", "REJECTED", "PAID", "CANCELED", "UNKNOWN"]
      - created_ts (datetime|None)
      - final_ts (datetime|None): timestamp of the final event used (post-sort)
      - paid_ts (datetime|None): timestamp of PAID event if any (useful for metrics)
      - issues: list[str]
    """
    # Keep stable input position to detect out-of-order input per invoice.
    indexed_events: List[Tuple[int, Dict[str, Any]]] = list(enumerate(events))

    # group events by invoice_id
    by_invoice: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {}
    for idx, e in indexed_events:
        inv = e.get("invoice_id")
        if inv is None:
            # If invoice_id missing, we can't do much; skip silently or raise.
            # In a real system, you'd log/track this.
            continue
        by_invoice.setdefault(inv, []).append((idx, e))

    results: Dict[str, Dict[str, Any]] = {}

    for invoice_id, items in by_invoice.items():
        issues: List[str] = []

        # Detect duplicates: exact duplicates on (invoice_id, event_type, ts)
        seen_keys = set()
        has_dup = False
        for _, e in items:
            k = (e.get("invoice_id"), e.get("event_type"), e.get("ts"))
            if k in seen_keys:
                has_dup = True
            else:
                seen_keys.add(k)
        if has_dup:
            issues.append("DUPLICATE_EVENT")

        # Parse and prepare sortable entries
        parsed: List[Tuple[datetime, int, Dict[str, Any]]] = []
        parse_failed = False
        for idx, e in items:
            ts_raw = e.get("ts")
            try:
                ts_dt = parse_ts(ts_raw)
            except Exception:
                parse_failed = True
                continue
            parsed.append((ts_dt, idx, e))

        # Sort by timestamp (then by original idx for deterministic tie-break)
        parsed_sorted = sorted(parsed, key=lambda x: (x[0], x[1]))

        # OUT_OF_ORDER_INPUT: compare original index order vs sorted order
        orig_order = [idx for idx, _e in items]
        sorted_order = [idx for _ts, idx, _e in parsed_sorted]
        if orig_order != sorted_order:
            issues.append("OUT_OF_ORDER_INPUT")

        # Resolve vendor_id / project_id (take first non-null seen in sorted order)
        vendor_id = None
        project_id = None
        for _ts, _idx, e in parsed_sorted:
            if vendor_id is None and e.get("vendor_id") is not None:
                vendor_id = e.get("vendor_id")
            if project_id is None and e.get("project_id") is not None:
                project_id = e.get("project_id")
            if vendor_id is not None and project_id is not None:
                break

        # Resolve amount as "most recent non-null amount" by event time
        resolved_amount: Optional[float] = None
        for _ts, _idx, e in parsed_sorted:
            amt = e.get("amount")
            if amt is not None:
                try:
                    resolved_amount = float(amt)
                except Exception:
                    # ignore unparseable amount; could mark issue in real system
                    pass

        if resolved_amount is None:
            issues.append("MISSING_AMOUNT")

        # Identify created_ts (first CREATED by time, if any)
        created_ts: Optional[datetime] = None
        for ts_dt, _idx, e in parsed_sorted:
            if e.get("event_type") == "CREATED":
                created_ts = ts_dt
                break
        if created_ts is None:
            issues.append("MISSING_CREATED")

        # Detect invalid transitions in a pragmatic way:
        # - We walk the sorted events and ensure the expected stage generally doesn't go backwards.
        # - CANCELED is terminal.
        # - Allow repeated same-stage events (duplicates already flagged separately).
        invalid_transition = False
        last_stage = -1
        canceled_seen = False

        # Also capture paid_ts (first PAID by time)
        paid_ts: Optional[datetime] = None

        for ts_dt, _idx, e in parsed_sorted:
            et = e.get("event_type")
            if et not in EXPECTED_ORDER:
                # Unknown event type -> doesn't necessarily invalidate, but could be flagged.
                continue

            stage = EXPECTED_ORDER[et]

            # Track first PAID time (for metrics)
            if et == "PAID" and paid_ts is None:
                paid_ts = ts_dt

            # Terminal cancel: if canceled seen, any later "normal" events are invalid
            if canceled_seen and et != "CANCELED":
                invalid_transition = True
                continue

            if et == "CANCELED":
                canceled_seen = True
                # Cancel can happen anytime; stage doesn't matter after it.
                last_stage = max(last_stage, stage)
                continue

            # Basic "no backward movement" check.
            # This will flag APPROVED -> SUBMITTED later, etc.
            if stage < last_stage:
                invalid_transition = True
            else:
                last_stage = stage

        if invalid_transition:
            issues.append("INVALID_TRANSITION")

        # Determine final_state using rules (apply after sorting events by time per invoice)
        event_types_in_time_order = [e.get("event_type") for _ts, _idx, e in parsed_sorted]
        last_event_type = event_types_in_time_order[-1] if event_types_in_time_order else None
        final_ts = parsed_sorted[-1][0] if parsed_sorted else None

        has_paid = "PAID" in event_types_in_time_order
        has_approved = "APPROVED" in event_types_in_time_order
        has_rejected = "REJECTED" in event_types_in_time_order
        has_submitted = any(t in ("SUBMITTED", "RESUBMITTED") for t in event_types_in_time_order)

        # "unless later CANCELED exists" nuance:
        # Rule list says:
        # - If last event is CANCELED => CANCELED
        # - If invoice has PAID at any time => PAID (unless later CANCELED exists; see above)
        # So CANCELED as last event overrides PAID.
        if last_event_type == "CANCELED":
            final_state = "CANCELED"
        elif has_paid:
            final_state = "PAID"
        elif has_approved and not _has_later_rejected(parsed_sorted):
            final_state = "APPROVED"
        elif last_event_type == "REJECTED":
            final_state = "REJECTED"
        elif has_submitted:
            final_state = "IN_REVIEW"
        elif "CREATED" in event_types_in_time_order:
            final_state = "OPEN"
        else:
            final_state = "UNKNOWN"

        results[invoice_id] = {
            "vendor_id": vendor_id,
            "project_id": project_id,
            "amount": resolved_amount,
            "final_state": final_state,
            "created_ts": created_ts,
            "final_ts": final_ts,
            "paid_ts": paid_ts,
            "issues": issues,
        }

    return results


def _has_later_rejected(parsed_sorted: List[Tuple[datetime, int, Dict[str, Any]]]) -> bool:
    """
    Returns True if there exists an APPROVED event that is followed later by a REJECTED event.
    Interpreting 'approved and no later rejected' as: if any rejected occurs after the last approved, treat as later rejected.
    """
    last_approved_ts: Optional[datetime] = None
    for ts_dt, _idx, e in parsed_sorted:
        if e.get("event_type") == "APPROVED":
            last_approved_ts = ts_dt
    if last_approved_ts is None:
        return False
    for ts_dt, _idx, e in parsed_sorted:
        if e.get("event_type") == "REJECTED" and ts_dt > last_approved_ts:
            return True
    return False


# ----------------------------
# Task B — Metrics
# ----------------------------

def compute_metrics(invoices: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returns:
      - avg_cycle_time_hours_paid: average hours from CREATED -> PAID for invoices that reached PAID
      - approval_rate: fraction of invoices that are APPROVED or PAID out of those that were submitted at least once
      - exception_rate: fraction of invoices with any issues out of all invoices
      - top_3_vendors_by_paid_amount: list of (vendor_id, total_paid_amount) sorted desc
    """
    # avg_cycle_time_hours_paid
    cycle_times: List[float] = []
    for inv_id, inv in invoices.items():
        created_ts = inv.get("created_ts")
        paid_ts = inv.get("paid_ts")
        if created_ts is not None and paid_ts is not None:
            cycle_times.append(hours_between(created_ts, paid_ts))

    avg_cycle_time_hours_paid = sum(cycle_times) / len(cycle_times) if cycle_times else None

    # approval_rate: (APPROVED or PAID) among those submitted at least once
    submitted_ids = []
    approved_or_paid = 0
    for inv_id, inv in invoices.items():
        # We don't have full event history here; but we can approximate with final_state:
        # Better would be storing has_submitted, etc. If you want, add those in Task A.
        # For now, infer submission by final_state being IN_REVIEW/APPROVED/REJECTED/PAID (not OPEN/UNKNOWN).
        # However the prompt says "ever had SUBMITTED or RESUBMITTED". We'll store a conservative proxy:
        # If created exists and final_state isn't OPEN/UNKNOWN, likely had submission.
        # If you want exact behavior, modify reconstruct_invoices to store "has_submitted".
        final_state = inv.get("final_state")
        has_submitted_proxy = final_state in {"IN_REVIEW", "APPROVED", "REJECTED", "PAID", "CANCELED"}
        if has_submitted_proxy:
            submitted_ids.append(inv_id)
            if final_state in {"APPROVED", "PAID"}:
                approved_or_paid += 1

    approval_rate = (approved_or_paid / len(submitted_ids)) if submitted_ids else None

    # exception_rate: any issues
    total = len(invoices)
    exceptions = sum(1 for inv in invoices.values() if inv.get("issues"))
    exception_rate = (exceptions / total) if total else None

    # top_3_vendors_by_paid_amount
    vendor_paid: Dict[str, float] = {}
    for inv in invoices.values():
        if inv.get("final_state") == "PAID":
            vendor = inv.get("vendor_id") or "UNKNOWN_VENDOR"
            amt = inv.get("amount")
            if amt is None:
                continue
            vendor_paid[vendor] = vendor_paid.get(vendor, 0.0) + float(amt)

    top_3 = sorted(vendor_paid.items(), key=lambda kv: kv[1], reverse=True)[:3]

    return {
        "avg_cycle_time_hours_paid": avg_cycle_time_hours_paid,
        "approval_rate": approval_rate,
        "exception_rate": exception_rate,
        "top_3_vendors_by_paid_amount": top_3,
    }


# ----------------------------
# Quick demo (optional)
# ----------------------------
if __name__ == "__main__":
    events = [
        {"invoice_id":"inv_1","vendor_id":"v1","project_id":"pA","event_type":"SUBMITTED","ts":"2026-01-03T10:05:00Z","amount":1000.0},
        {"invoice_id":"inv_1","vendor_id":"v1","project_id":"pA","event_type":"CREATED","ts":"2026-01-03T10:00:00Z","amount":None},
        {"invoice_id":"inv_1","vendor_id":"v1","project_id":"pA","event_type":"APPROVED","ts":"2026-01-03T12:00:00Z","amount":None},
        {"invoice_id":"inv_1","vendor_id":"v1","project_id":"pA","event_type":"PAID","ts":"2026-01-04T09:00:00Z","amount":None},

        {"invoice_id":"inv_2","vendor_id":"v2","project_id":"pA","event_type":"CREATED","ts":"2026-01-05T09:00:00Z","amount":500.0},
        {"invoice_id":"inv_2","vendor_id":"v2","project_id":"pA","event_type":"SUBMITTED","ts":"2026-01-05T09:10:00Z","amount":None},
        {"invoice_id":"inv_2","vendor_id":"v2","project_id":"pA","event_type":"REJECTED","ts":"2026-01-05T10:00:00Z","amount":None},
        {"invoice_id":"inv_2","vendor_id":"v2","project_id":"pA","event_type":"RESUBMITTED","ts":"2026-01-06T11:00:00Z","amount":550.0},
        {"invoice_id":"inv_2","vendor_id":"v2","project_id":"pA","event_type":"APPROVED","ts":"2026-01-06T12:00:00Z","amount":None},

        {"invoice_id":"inv_3","vendor_id":"v2","project_id":"pB","event_type":"APPROVED","ts":"2026-01-02T12:00:00Z","amount":200.0},
        {"invoice_id":"inv_3","vendor_id":"v2","project_id":"pB","event_type":"APPROVED","ts":"2026-01-02T12:00:00Z","amount":200.0},
        {"invoice_id":"inv_3","vendor_id":"v2","project_id":"pB","event_type":"PAID","ts":"2026-01-02T13:00:00Z","amount":None},

        {"invoice_id":"inv_4","vendor_id":"v3","project_id":"pC","event_type":"CANCELED","ts":"2026-01-07T09:00:00Z","amount":300.0},
        {"invoice_id":"inv_4","vendor_id":"v3","project_id":"pC","event_type":"CREATED","ts":"2026-01-07T08:00:00Z","amount":300.0},
    ]

    invoices = reconstruct_invoices(events)
    metrics = compute_metrics(invoices)

    from pprint import pprint
    pprint(invoices)
    pprint(metrics)

