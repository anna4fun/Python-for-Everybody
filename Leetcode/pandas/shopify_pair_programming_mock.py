"""
Shopify pair-programming mock (Pandas/Numpy)

You are given 2 tables:

1) ad_buckets
   - user_id (int)
   - ad_bucket (str)              # cohort assignment (e.g., "A", "B")
   - first_expose_date (datetime) # first time the user was eligible/exposed to ads
   (Extension in Q4: add `experiment` like "Treatment"/"Control".)

2) streams
   - user_id (int)
   - date (datetime)              # when the stream happened
   - surface (str)                # surface area where the stream originated (e.g., "home", "search")
   - ms_played (int)              # how long the user played (milliseconds)

Business rules / assumptions for this mock (state these out loud in an interview):
- A "qualified stream" for stream-rate purposes has ms_played >= min_ms_played (default: 30_000 ms).
  (For "average stream time" in Q2, we use *all* ms_played > 0 by default.)
- A stream is attributable/valid only if date >= first_expose_date for that user.
  If first_expose_date > date, that stream is an invalid trigger and must be excluded (Q4 discusses this).
- Stream rate is computed per (ad_bucket, surface) as:
    numerator   = distinct users in that ad_bucket who have >=1 qualified, valid stream on that surface
    denominator = distinct users in that ad_bucket (regardless of surface)
    stream_rate = numerator / denominator

Questions
1) Compute stream rate per (ad_bucket, surface).
2) Write a function that returns week-over-week % change in *weekly average stream time* for each surface.
   - Define week as starting on Monday.
   - Compute per surface & week:
       user_week_ms = sum(ms_played) per (user_id, surface, week)
       weekly_avg_ms = mean(user_week_ms) across users active on that surface in that week
       wow_pct = (weekly_avg_ms - prev_weekly_avg_ms) / prev_weekly_avg_ms
3) Extend Q2 to handle multiple surfaces in one call (e.g., surfaces=["home","search"] or None for all).
4) Make Q2/Q3 more flexible:
   - allow extra grouping columns (e.g., experiment, ad_bucket)
   - handle invalid triggers (first_expose_date > date) via drop/flag strategies
   - make it easy to add new dimensions without rewriting the function
5) Apply + lambda across multiple columns:
   Create a new column using a custom Python function that depends on multiple columns.
   Example rule-set for `adjusted_ms_played` (feel free to change the rules during practice):
   - if surface == "home" and ad_bucket == "A": adjusted_ms_played = int(ms_played * 1.10)
   - elif surface == "search" and ad_bucket == "B": adjusted_ms_played = ms_played + 5_000
   - else: adjusted_ms_played = ms_played
   Implement with `df.apply(lambda row: ..., axis=1)`. Bonus: rewrite without row-wise apply.

This file is intentionally an exercise scaffold: implement the TODOs and run it.
"""

from __future__ import annotations
from uu import Error

from matplotlib import axis
import pandas as pd
import numpy as np
import datetime as dt


def make_sample_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    ad_buckets = pd.DataFrame(
        [
            {"user_id": 1, "ad_bucket": "A", "first_expose_date": "2026-01-05"},
            {"user_id": 2, "ad_bucket": "A", "first_expose_date": "2026-01-05"},
            {"user_id": 3, "ad_bucket": "B", "first_expose_date": "2026-01-05"},
            {"user_id": 4, "ad_bucket": "B", "first_expose_date": "2026-01-12"},
            {"user_id": 5, "ad_bucket": "B", "first_expose_date": "2026-01-05"},
        ]
    )

    streams = pd.DataFrame(
        [
            # Week of 2026-01-05 (Mon)
            {"user_id": 1, "date": "2026-01-06", "surface": "home", "ms_played": 60_000},
            {"user_id": 2, "date": "2026-01-07", "surface": "home", "ms_played": 30_000},
            {"user_id": 3, "date": "2026-01-08", "surface": "home", "ms_played": 50_000},
            {"user_id": 5, "date": "2026-01-06", "surface": "search", "ms_played": 10_000},
            {"user_id": 5, "date": "2026-01-07", "surface": "search", "ms_played": 45_000},
            # Invalid trigger: stream before first_expose_date (user 4 first exposed 2026-01-12)
            {"user_id": 4, "date": "2026-01-10", "surface": "home", "ms_played": 70_000},
            # Week of 2026-01-12
            {"user_id": 4, "date": "2026-01-12", "surface": "home", "ms_played": 35_000},
            {"user_id": 3, "date": "2026-01-16", "surface": "home", "ms_played": 20_000},
            {"user_id": 1, "date": "2026-01-13", "surface": "search", "ms_played": 40_000},
            # Week of 2026-01-19
            {"user_id": 1, "date": "2026-01-20", "surface": "home", "ms_played": 80_000},
            {"user_id": 3, "date": "2026-01-21", "surface": "home", "ms_played": 60_000},
            {"user_id": 5, "date": "2026-01-19", "surface": "search", "ms_played": 30_000},
        ]
    )

    ad_buckets["first_expose_date"] = pd.to_datetime(ad_buckets["first_expose_date"])
    streams["date"] = pd.to_datetime(streams["date"])
    return ad_buckets, streams

ad_buckets, streams = make_sample_data()

def compute_stream_rate(
    ad_buckets: pd.DataFrame,
    streams: pd.DataFrame,
    *,
    min_ms_played: int = 30_000,
) -> pd.DataFrame:
    """
    Q1: Return stream rate per (ad_bucket, surface).

    Output columns:
    - ad_bucket
    - surface
    - n_users (denominator)
    - n_streamers (numerator)
    - stream_rate
    """
    try:
        raw_df = ad_buckets.merge(streams, on=['user_id'], how='left')
        raw_df.shape
        # remove invalid triggers: streams before first_expose_date
        raw_df = raw_df[raw_df['date'] >= raw_df['first_expose_date']]
        # remove invalid streams: ms_played < min_ms_played
        raw_df = raw_df[raw_df['ms_played'] >= min_ms_played]
        raw_df.shape
        # compute aggregation
        bucket_df = raw_df.groupby(['ad_bucket']).agg({'user_id': 'nunique'}).reset_index().rename(columns={'user_id': 'n_users'})
        bucket_surface_df = raw_df.groupby(['ad_bucket', 'surface']).agg({'user_id': 'nunique'}).reset_index().rename(columns={'user_id': 'n_streamers'})
        agg_df = bucket_df.merge(bucket_surface_df, on=['ad_bucket'], how='left')
        agg_df = agg_df[['ad_bucket', 'surface', 'n_users', 'n_streamers']]
        agg_df['stream_rate'] = round(agg_df['n_streamers'] / agg_df['n_users'], 2)
        return agg_df
    except Exception as e:
        print(e)
        return None

stream_rate = compute_stream_rate(ad_buckets, streams)
print(stream_rate)

def weekly_avg_stream_time_wow(
    ad_buckets: pd.DataFrame,
    streams: pd.DataFrame,
    *,
    surfaces: list[str] | None = None,
    include_group_cols: list[str] | None = None,
    min_ms_played: int = 1,
) -> pd.DataFrame:
    """
    Q2/Q3/Q4:
    Compute week-over-week % change in weekly average stream time.

    Required behavior:
    - Filter invalid triggers: keep only rows where date >= first_expose_date
    - If `surfaces` is not None, filter streams to those surfaces
    - Week starts Monday
    - Compute:
        user_week_ms = sum(ms_played) per (user_id, surface, week_start, *include_group_cols)
        weekly_avg_ms = mean(user_week_ms) across users per (surface, week_start, *include_group_cols)
        wow_pct = pct change vs previous week within each (surface, *include_group_cols)

    Suggested output columns:
    - surface
    - week_start
    - weekly_avg_ms
    - wow_pct
    - plus any `include_group_cols` (e.g., ["ad_bucket"] or ["experiment"])
    """
    raw_df = ad_buckets.merge(streams, on=["user_id"], how="left")

    # Filter invalid triggers.
    raw_df = raw_df[raw_df["date"] >= raw_df["first_expose_date"]]

    # Optional surface filter.
    if surfaces is not None:
        raw_df = raw_df[raw_df["surface"].isin(surfaces)]

    # Exclude non-positive / invalid playtime.
    raw_df = raw_df[raw_df["ms_played"] >= min_ms_played]

    # Week starts Monday.
    raw_df["week_start"] = raw_df["date"].dt.to_period("W").dt.start_time

    include_group_cols=None
    extra_group_cols = include_group_cols or []
    dims = ["surface", "week_start", *extra_group_cols]

    # user_week_ms: sum per user/week (then weekly_avg_ms is mean across users, like SQL AVG over user-level totals).
    user_week = (
        raw_df.groupby(["user_id", *dims], as_index=False)
        .agg({'ms_played':'sum'})
        .rename(columns={"ms_played": "user_week_ms"})
    )

    agg_df = (
        user_week.groupby(dims, as_index=False)
        .agg({'user_week_ms':'mean'})
        .rename(columns={"user_week_ms": "weekly_avg_ms"})
    )

    agg_df = agg_df.sort_values(dims, ascending=[True] * len(dims))
    wow_group_cols = ["surface", *extra_group_cols]
    agg_df["wow_pct"] = agg_df.groupby(wow_group_cols)['weekly_avg_ms'].pct_change(periods=1) # periods = offset, periods=1 prev row 1, periods=2 next row 2
    return agg_df[["surface", "week_start", *extra_group_cols, "weekly_avg_ms", "wow_pct"]]

def adjust(ms_played: int, surface: str, ad_bucket: str) -> int:
    """
    Rule-set (same as the prompt at the top of this file):
      - if surface == "home" and ad_bucket == "A": adjusted = int(ms_played * 1.10)
      - elif surface == "search" and ad_bucket == "B": adjusted = ms_played + 5_000
      - else: adjusted = ms_played
    """
    if  surface == "home" and ad_bucket == "A":
        return int(ms_played * 1.10)
    elif surface == "search" and ad_bucket == "B": 
        return ms_played + 5_000
    else:
        return ms_played

def add_adjusted_ms_played_exercise(
    ad_buckets: pd.DataFrame,
    streams: pd.DataFrame,
    *,
    out_col: str = "adjusted_ms_played",
) -> pd.DataFrame:
    """
    Q5 exercise:
    - Join streams to ad_buckets on user_id to get `ad_bucket` per stream row
    - Filter invalid triggers (keep date >= first_expose_date)
    - Create `out_col` using a custom function + apply/lambda across columns

    Rule-set (same as the prompt at the top of this file):
      - if surface == "home" and ad_bucket == "A": adjusted = int(ms_played * 1.10)
      - elif surface == "search" and ad_bucket == "B": adjusted = ms_played + 5_000
      - else: adjusted = ms_played

    Suggested skeleton:
        df = ad_buckets.merge(streams, on="user_id", how="left")
        df = df[df["date"] >= df["first_expose_date"]]

        def adjust(ms_played: int, surface: str, ad_bucket: str) -> int:
            ...

        df[out_col] = df.apply(lambda r: adjust(r["ms_played"], r["surface"], r["ad_bucket"]), axis=1)
        return df

    Expected output: a per-stream DataFrame that contains at least:
    - user_id, ad_bucket, first_expose_date, date, surface, ms_played, out_col
    """
    try:
        raw_df = ad_buckets.merge(streams, on=['user_id'], how='left')
        raw_df = raw_df[raw_df['first_expose_date'] <= raw_df['date']]
        raw_df['out_col'] = raw_df.apply(lambda d: adjust(d['ms_played'], d['surface'], d['ad_bucket']), axis=1)
        return raw_df
    except Error as e:
        print(e)
        return None


def _expected_stream_rate_for_sample() -> pd.DataFrame:
    # Denominators: bucket A has 2 users; bucket B has 3 users.
    # Numerators based on qualified streams (ms_played >= 30_000) and valid triggers (date >= first_expose_date):
    # - bucket A, home: users 1 & 2 => 2/2
    # - bucket A, search: user 1 => 1/2
    # - bucket B, home: users 3 & 4 => 2/3 (user 4's 2026-01-10 stream is invalid; 2026-01-12 is valid)
    # - bucket B, search: user 5 => 1/3
    return pd.DataFrame(
        [
            {"ad_bucket": "A", "surface": "home", "n_users": 2, "n_streamers": 2, "stream_rate": 1.0},
            {"ad_bucket": "A", "surface": "search", "n_users": 2, "n_streamers": 1, "stream_rate": 0.5},
            {"ad_bucket": "B", "surface": "home", "n_users": 3, "n_streamers": 2, "stream_rate": round(2 / 3, 2)},
            {"ad_bucket": "B", "surface": "search", "n_users": 3, "n_streamers": 1, "stream_rate": round(1 / 3, 2)},
        ]
    ).sort_values(["ad_bucket", "surface"], ignore_index=True)


def _expected_wow_for_sample() -> pd.DataFrame:
    # Week starts Monday. Expected weekly_avg_ms computed from user_week_ms sums (post-exposure only).
    # home:
    #   2026-01-05: user1=60000, user2=30000, user3=50000 => avg=46666.6667
    #   2026-01-12: user3=20000, user4=35000 => avg=27500; wow=-0.4107142857
    #   2026-01-19: user1=80000, user3=60000 => avg=70000; wow=1.5454545455
    # search:
    #   2026-01-05: user5=55000 => avg=55000
    #   2026-01-12: user1=40000 => avg=40000; wow=-0.2727272727
    #   2026-01-19: user5=30000 => avg=30000; wow=-0.25
    return pd.DataFrame(
        [
            {"surface": "home", "week_start": "2026-01-05", "weekly_avg_ms": 46_666.666666666664, "wow_pct": None},
            {"surface": "home", "week_start": "2026-01-12", "weekly_avg_ms": 27_500.0, "wow_pct": -0.4107142857142857},
            {"surface": "home", "week_start": "2026-01-19", "weekly_avg_ms": 70_000.0, "wow_pct": 1.5454545454545454},
            {"surface": "search", "week_start": "2026-01-05", "weekly_avg_ms": 55_000.0, "wow_pct": None},
            {"surface": "search", "week_start": "2026-01-12", "weekly_avg_ms": 40_000.0, "wow_pct": -0.2727272727272727},
            {"surface": "search", "week_start": "2026-01-19", "weekly_avg_ms": 30_000.0, "wow_pct": -0.25},
        ]
    ).assign(week_start=lambda d: pd.to_datetime(d["week_start"])).sort_values(
        ["surface", "week_start"], ignore_index=True
    )


def run_self_check() -> None:
    ad_buckets, streams = make_sample_data()

    got_rate = compute_stream_rate(ad_buckets, streams).sort_values(["ad_bucket", "surface"], ignore_index=True)
    exp_rate = _expected_stream_rate_for_sample()
    pd.testing.assert_frame_equal(got_rate, exp_rate, check_exact=False, rtol=1e-9, atol=1e-9)

    got_wow = weekly_avg_stream_time_wow(ad_buckets, streams).sort_values(["surface", "week_start"], ignore_index=True)
    exp_wow = _expected_wow_for_sample()
    pd.testing.assert_frame_equal(got_wow, exp_wow, check_exact=False, rtol=1e-9, atol=1e-9)


if __name__ == "__main__":
    ad_buckets_df, streams_df = make_sample_data()
    print("Sample ad_buckets:")
    print(ad_buckets_df)
    print("\nSample streams:")
    print(streams_df)

    try:
        run_self_check()
        print("\nSelf-check passed.")
    except NotImplementedError:
        print("\nTODO: implement `compute_stream_rate` and `weekly_avg_stream_time_wow`, then rerun this script.")
