from __future__ import annotations

import csv
import datetime as dt
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List


OUTPUT_CSV = "daily_app_store_metrics.csv"
START_DATE = dt.date(2023, 1, 1)
END_DATE = dt.date(2025, 12, 31)

SPIKE_START = dt.date(2025, 8, 15)
SPIKE_END = dt.date(2025, 9, 10)


@dataclass(frozen=True)
class Segment:
    name: str
    share: float
    atc_delta: float = 0.0
    checkout_delta: float = 0.0
    pv_delta: float = 0.0
    aov_delta: float = 0.0
    spike_sessions_boost: float = 1.0


CHANNELS: List[Segment] = [
    Segment("organic", 0.38, atc_delta=0.025, checkout_delta=0.015, pv_delta=0.12, spike_sessions_boost=1.1),
    Segment("paid_search", 0.24, atc_delta=0.000, checkout_delta=-0.005, pv_delta=0.04, spike_sessions_boost=1.8),
    Segment("email", 0.07, atc_delta=0.032, checkout_delta=0.020, pv_delta=0.10, spike_sessions_boost=1.0),
    Segment("affiliate", 0.10, atc_delta=-0.018, checkout_delta=-0.010, pv_delta=-0.03, spike_sessions_boost=2.2),
    Segment("referral", 0.09, atc_delta=-0.020, checkout_delta=-0.015, pv_delta=-0.06, spike_sessions_boost=2.5),
    Segment("social", 0.08, atc_delta=-0.012, checkout_delta=-0.010, pv_delta=-0.04, spike_sessions_boost=1.5),
    Segment("direct", 0.04, atc_delta=0.010, checkout_delta=0.005, pv_delta=0.06, spike_sessions_boost=1.0),
]

DEVICES: List[Segment] = [
    Segment("mobile", 0.62, atc_delta=-0.012, checkout_delta=-0.008, pv_delta=-0.02, aov_delta=-2.0, spike_sessions_boost=1.25),
    Segment("desktop", 0.30, atc_delta=0.015, checkout_delta=0.010, pv_delta=0.10, aov_delta=2.5, spike_sessions_boost=1.0),
    Segment("tablet", 0.08, atc_delta=0.003, checkout_delta=0.004, pv_delta=0.05, aov_delta=1.0, spike_sessions_boost=1.05),
]

GEOS: List[Segment] = [
    Segment("US", 0.52, atc_delta=0.012, checkout_delta=0.006, aov_delta=3.0, spike_sessions_boost=1.1),
    Segment("CA", 0.10, atc_delta=0.007, checkout_delta=0.004, aov_delta=2.0, spike_sessions_boost=1.05),
    Segment("UK", 0.11, atc_delta=0.009, checkout_delta=0.005, aov_delta=2.5, spike_sessions_boost=1.05),
    Segment("AU", 0.07, atc_delta=0.010, checkout_delta=0.006, aov_delta=2.0, spike_sessions_boost=1.05),
    Segment("IN", 0.12, atc_delta=-0.010, checkout_delta=-0.007, aov_delta=-4.0, spike_sessions_boost=1.4),
    Segment("BR", 0.08, atc_delta=-0.007, checkout_delta=-0.006, aov_delta=-3.0, spike_sessions_boost=1.3),
]

MERCHANT_TIERS: List[Segment] = [
    Segment("trial", 0.45, atc_delta=-0.015, checkout_delta=-0.012, pv_delta=-0.06, aov_delta=-5.0, spike_sessions_boost=1.2),
    Segment("basic", 0.37, atc_delta=0.005, checkout_delta=0.003, pv_delta=0.02, aov_delta=0.0, spike_sessions_boost=1.05),
    Segment("plus", 0.18, atc_delta=0.022, checkout_delta=0.015, pv_delta=0.08, aov_delta=8.0, spike_sessions_boost=0.95),
]

LANDING_WEIGHTS_BY_CHANNEL: Dict[str, Dict[str, float]] = {
    "organic": {"home": 0.20, "category_page": 0.34, "product_page": 0.26, "campaign_lp": 0.05, "blog_article": 0.15},
    "paid_search": {"home": 0.06, "category_page": 0.18, "product_page": 0.22, "campaign_lp": 0.49, "blog_article": 0.05},
    "email": {"home": 0.08, "category_page": 0.15, "product_page": 0.30, "campaign_lp": 0.40, "blog_article": 0.07},
    "affiliate": {"home": 0.05, "category_page": 0.12, "product_page": 0.20, "campaign_lp": 0.58, "blog_article": 0.05},
    "referral": {"home": 0.12, "category_page": 0.25, "product_page": 0.25, "campaign_lp": 0.30, "blog_article": 0.08},
    "social": {"home": 0.10, "category_page": 0.15, "product_page": 0.18, "campaign_lp": 0.44, "blog_article": 0.13},
    "direct": {"home": 0.35, "category_page": 0.25, "product_page": 0.28, "campaign_lp": 0.06, "blog_article": 0.06},
}

LANDING_ATC_DELTA: Dict[str, float] = {
    "home": 0.004,
    "category_page": 0.010,
    "product_page": 0.021,
    "campaign_lp": -0.016,
    "blog_article": -0.022,
}

APP_CATEGORY_WEIGHTS_BY_GEO: Dict[str, Dict[str, float]] = {
    "US": {"productivity": 0.26, "finance": 0.22, "lifestyle": 0.16, "education": 0.14, "gaming": 0.22},
    "CA": {"productivity": 0.27, "finance": 0.18, "lifestyle": 0.16, "education": 0.18, "gaming": 0.21},
    "UK": {"productivity": 0.25, "finance": 0.23, "lifestyle": 0.17, "education": 0.13, "gaming": 0.22},
    "AU": {"productivity": 0.24, "finance": 0.19, "lifestyle": 0.18, "education": 0.15, "gaming": 0.24},
    "IN": {"productivity": 0.23, "finance": 0.15, "lifestyle": 0.14, "education": 0.21, "gaming": 0.27},
    "BR": {"productivity": 0.21, "finance": 0.16, "lifestyle": 0.17, "education": 0.14, "gaming": 0.32},
}

APP_CATEGORY_ATC_DELTA: Dict[str, float] = {
    "productivity": 0.010,
    "finance": 0.004,
    "lifestyle": 0.000,
    "education": 0.006,
    "gaming": -0.010,
}

APP_CATEGORY_BASE_AOV: Dict[str, float] = {
    "productivity": 48.0,
    "finance": 54.0,
    "lifestyle": 41.0,
    "education": 36.0,
    "gaming": 32.0,
}


def date_range(start_date: dt.date, end_date: dt.date) -> Iterable[dt.date]:
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += dt.timedelta(days=1)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def weighted_pick(weights: Dict[str, float], rng: random.Random) -> str:
    total_weight = sum(weights.values())
    threshold = rng.random() * total_weight
    cumulative = 0.0
    for key, weight in weights.items():
        cumulative += weight
        if cumulative >= threshold:
            return key
    return next(iter(weights.keys()))


def is_spike_day(day: dt.date) -> bool:
    return SPIKE_START <= day <= SPIKE_END


def seasonality_factor(day: dt.date) -> float:
    day_of_year = day.timetuple().tm_yday
    yearly = 0.12 * math.sin(2 * math.pi * day_of_year / 365.25)
    semiannual = 0.05 * math.cos(4 * math.pi * day_of_year / 365.25)
    weekend = 0.90 if day.weekday() >= 5 else 1.0
    q4_uplift = 1.13 if day.month in (11, 12) else 1.0
    return (1.0 + yearly + semiannual) * weekend * q4_uplift


def generate_csv(output_path: str, seed: int = 42) -> Dict[str, float]:
    rng = random.Random(seed)
    day_count = (END_DATE - START_DATE).days

    fieldnames = [
        "date",
        "sessions",
        "product_views",
        "add_to_cart",
        "purchases",
        "revenue",
        "channel",
        "device_type",
        "geo",
        "merchant_tier",
        "landing_page",
        "app_category",
        "is_bot_suspected",
    ]

    pre_spike_start = SPIKE_START - dt.timedelta(days=42)
    pre_spike_end = SPIKE_START - dt.timedelta(days=1)
    period_totals: Dict[str, Dict[str, float]] = {
        "pre": {"sessions": 0.0, "product_views": 0.0, "add_to_cart": 0.0, "purchases": 0.0, "days": 0.0},
        "spike": {"sessions": 0.0, "product_views": 0.0, "add_to_cart": 0.0, "purchases": 0.0, "days": 0.0},
    }

    row_count = 0
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for current_date in date_range(START_DATE, END_DATE):
            days_since_start = (current_date - START_DATE).days
            growth_factor = 1.0 + 0.16 * (days_since_start / day_count)
            day_base_sessions = 19500 * seasonality_factor(current_date) * growth_factor
            if is_spike_day(current_date):
                day_base_sessions *= 1.25

            day_sessions_total = 0.0
            day_views_total = 0.0
            day_atc_total = 0.0
            day_purchases_total = 0.0

            for channel in CHANNELS:
                for device in DEVICES:
                    for geo in GEOS:
                        for tier in MERCHANT_TIERS:
                            segment_share = channel.share * device.share * geo.share * tier.share
                            expected_sessions = day_base_sessions * segment_share
                            if is_spike_day(current_date):
                                expected_sessions *= channel.spike_sessions_boost * device.spike_sessions_boost
                                expected_sessions *= geo.spike_sessions_boost * tier.spike_sessions_boost
                            expected_sessions *= rng.uniform(0.86, 1.18)

                            sessions = max(0, int(round(expected_sessions)))
                            if sessions == 0:
                                continue

                            landing_page = weighted_pick(LANDING_WEIGHTS_BY_CHANNEL[channel.name], rng)
                            app_category = weighted_pick(APP_CATEGORY_WEIGHTS_BY_GEO[geo.name], rng)

                            bot_probability = 0.006
                            if channel.name in {"affiliate", "referral", "social"}:
                                bot_probability += 0.012
                            if device.name == "mobile":
                                bot_probability += 0.006
                            if geo.name in {"IN", "BR"}:
                                bot_probability += 0.008
                            if is_spike_day(current_date):
                                bot_probability += 0.010
                                if channel.name in {"affiliate", "referral"}:
                                    bot_probability += 0.085
                            is_bot_suspected = rng.random() < clamp(bot_probability, 0.0, 0.35)

                            pv_per_session = 1.48 + channel.pv_delta + device.pv_delta + tier.pv_delta
                            pv_per_session += rng.uniform(-0.08, 0.08)
                            if is_spike_day(current_date):
                                pv_per_session += 0.32
                            if is_bot_suspected:
                                pv_per_session -= 0.12
                            pv_per_session = clamp(pv_per_session, 0.9, 2.1)
                            product_views = max(sessions, int(round(sessions * pv_per_session)))

                            atc_rate = 0.102
                            atc_rate += channel.atc_delta + device.atc_delta + geo.atc_delta + tier.atc_delta
                            atc_rate += LANDING_ATC_DELTA[landing_page] + APP_CATEGORY_ATC_DELTA[app_category]
                            if is_spike_day(current_date):
                                atc_rate -= 0.015
                                if channel.name in {"affiliate", "referral", "social"}:
                                    atc_rate -= 0.008
                            if is_bot_suspected:
                                atc_rate -= 0.030
                            atc_rate = clamp(atc_rate, 0.006, 0.30)

                            add_to_cart = int(round(product_views * atc_rate * rng.uniform(0.93, 1.08)))
                            add_to_cart = clamp(add_to_cart, 0, product_views)
                            add_to_cart = int(add_to_cart)

                            checkout_rate = 0.235 + channel.checkout_delta + device.checkout_delta
                            checkout_rate += geo.checkout_delta + tier.checkout_delta
                            checkout_rate += APP_CATEGORY_ATC_DELTA[app_category] * 0.3
                            if is_spike_day(current_date):
                                checkout_rate += 0.002
                            if is_bot_suspected:
                                checkout_rate -= 0.045
                            checkout_rate = clamp(checkout_rate, 0.02, 0.88)

                            purchases = int(round(add_to_cart * checkout_rate * rng.uniform(0.94, 1.06)))
                            purchases = int(clamp(purchases, 0, add_to_cart))

                            avg_order_value = APP_CATEGORY_BASE_AOV[app_category] + device.aov_delta + tier.aov_delta + geo.aov_delta
                            avg_order_value += rng.uniform(-2.5, 2.5)
                            avg_order_value = max(8.0, avg_order_value)
                            revenue = round(purchases * avg_order_value, 2)

                            row = {
                                "date": current_date.isoformat(),
                                "sessions": sessions,
                                "product_views": product_views,
                                "add_to_cart": add_to_cart,
                                "purchases": purchases,
                                "revenue": revenue,
                                "channel": channel.name,
                                "device_type": device.name,
                                "geo": geo.name,
                                "merchant_tier": tier.name,
                                "landing_page": landing_page,
                                "app_category": app_category,
                                "is_bot_suspected": str(is_bot_suspected).lower(),
                            }
                            writer.writerow(row)
                            row_count += 1

                            day_sessions_total += sessions
                            day_views_total += product_views
                            day_atc_total += add_to_cart
                            day_purchases_total += purchases

            period_key = None
            if pre_spike_start <= current_date <= pre_spike_end:
                period_key = "pre"
            elif is_spike_day(current_date):
                period_key = "spike"

            if period_key:
                period_totals[period_key]["sessions"] += day_sessions_total
                period_totals[period_key]["product_views"] += day_views_total
                period_totals[period_key]["add_to_cart"] += day_atc_total
                period_totals[period_key]["purchases"] += day_purchases_total
                period_totals[period_key]["days"] += 1

    pre = period_totals["pre"]
    spike = period_totals["spike"]
    summary = {
        "rows": float(row_count),
        "pre_avg_sessions_per_day": pre["sessions"] / max(1.0, pre["days"]),
        "spike_avg_sessions_per_day": spike["sessions"] / max(1.0, spike["days"]),
        "pre_atc_rate": pre["add_to_cart"] / max(1.0, pre["product_views"]),
        "spike_atc_rate": spike["add_to_cart"] / max(1.0, spike["product_views"]),
        "pre_cvr": pre["purchases"] / max(1.0, pre["sessions"]),
        "spike_cvr": spike["purchases"] / max(1.0, spike["sessions"]),
    }
    return summary


def main() -> None:
    summary = generate_csv(OUTPUT_CSV)
    print(f"Created {OUTPUT_CSV}")
    print(f"Rows: {int(summary['rows'])}")
    print(
        "Avg sessions/day pre-spike vs spike: "
        f"{summary['pre_avg_sessions_per_day']:.0f} -> {summary['spike_avg_sessions_per_day']:.0f}"
    )
    print(f"ATC rate pre-spike vs spike: {summary['pre_atc_rate']:.3%} -> {summary['spike_atc_rate']:.3%}")
    print(f"CVR pre-spike vs spike: {summary['pre_cvr']:.3%} -> {summary['spike_cvr']:.3%}")


if __name__ == "__main__":
    main()
