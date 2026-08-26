"""X4 summariser: (a) day coverage, (b) event counts + v3-vs-v4 delta, (c) range alignment,
then the per-month count summaries. Reads only x4 artifacts."""
import sys, json
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")
pl.Config.set_tbl_rows(200); pl.Config.set_tbl_cols(30)
pl.Config.set_fmt_str_lengths(40); pl.Config.set_ascii_tables(True); pl.Config.set_tbl_width_chars(200)

OUT = Path(__file__).resolve().parent
d = pl.read_csv(OUT / "per_day_coverage.csv")
logs = json.loads((OUT / "run_logs.json").read_text(encoding="utf-8"))
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]

print("=" * 110)
print("(a) DAY COVERAGE  — lattice dates vs v4 per-day MBO files")
print("=" * 110)
cov = []
for m in MONTHS:
    s = d.filter(pl.col("month") == m)
    lat_days = s.filter(pl.col("in_lattice"))
    v4d = s.filter(pl.col("v4_day_file_present"))
    miss = lat_days.filter(~pl.col("v4_day_file_present"))
    extra = v4d.filter(~pl.col("in_lattice"))
    cov.append(dict(
        month=m,
        lattice_days=lat_days.height, v4_day_files=v4d.height,
        both=lat_days.filter(pl.col("v4_day_file_present")).height,
        lattice_only=miss.height, v4_only=extra.height,
        lattice_rows_total=int(lat_days["lattice_rows"].sum()),
        lattice_rows_on_uncovered_days=int(miss["lattice_rows"].sum()),
        pct_lattice_rows_uncovered=round(100 * miss["lattice_rows"].sum()
                                         / lat_days["lattice_rows"].sum(), 3),
        lattice_only_dates=";".join(miss["date"].to_list()),
        v4_only_dates=";".join(extra["date"].to_list())))
cv = pl.DataFrame(cov)
print(cv.select(["month", "lattice_days", "v4_day_files", "both", "lattice_only", "v4_only",
                 "lattice_rows_total", "lattice_rows_on_uncovered_days",
                 "pct_lattice_rows_uncovered"]))
print()
for r in cov:
    print(f"  {r['month']}  lattice-only dates ({r['lattice_only']}): {r['lattice_only_dates']}")
    if r["v4_only"]:
        print(f"           v4-only dates ({r['v4_only']}): {r['v4_only_dates']}")
cv.write_csv(OUT / "soundness_a_day_coverage.csv")

print()
print("=" * 110)
print("(b) EVENT COUNTS IN THE JOINED WINDOW  (UTC hours [14,22) on days present in BOTH)")
print("=" * 110)
b = []
for m in MONTHS:
    s = d.filter((pl.col("month") == m) & pl.col("in_lattice") & pl.col("v4_day_file_present"))
    sall = d.filter((pl.col("month") == m) & pl.col("in_lattice"))
    v4 = int(s["v4_events_in_window"].sum()); v3 = int(s["v3_events_in_window"].sum())
    v3all = int(sall["v3_events_in_window"].sum())
    lg = logs["months"][m]
    b.append(dict(month=m, joined_days=s.height,
                  v4_events_joined_window=v4, v3_events_joined_window=v3,
                  delta_v4_minus_v3=v4 - v3,
                  pct_delta=round(100 * (v4 - v3) / v3, 4) if v3 else None,
                  v3_events_all_lattice_days=v3all,
                  v3_events_on_v4_uncovered_days=v3all - v3,
                  v4_file_rows_total=lg["v4_total_rows"],
                  v3_file_rows_total=lg["v3_total_rows"]))
bb = pl.DataFrame(b)
print(bb)
bb.write_csv(OUT / "soundness_b_event_counts.csv")
print("\n  per-day v4-minus-v3 delta distribution (joined days only):")
j = d.filter(pl.col("in_lattice") & pl.col("v4_day_file_present")
             & pl.col("v3_events_in_window").is_not_null())
j = j.with_columns((pl.col("v4_events_in_window") - pl.col("v3_events_in_window")).alias("dlt"),
                   (100 * (pl.col("v4_events_in_window") - pl.col("v3_events_in_window"))
                    / pl.col("v3_events_in_window")).alias("pct"))
print(j.select(["dlt", "pct"]).describe())
print("\n  the 10 days with the largest |pct| delta:")
print(j.sort(pl.col("pct").abs(), descending=True)
       .select(["month", "date", "v4_events_in_window", "v3_events_in_window", "dlt", "pct"])
       .head(10))

print()
print("=" * 110)
print("(c) PER-DAY TIMESTAMP-RANGE ALIGNMENT inside the window")
print("=" * 110)
c = j.with_columns(
    pl.col("lattice_min").str.slice(11, 12).alias("lat_from"),
    pl.col("v4_min").str.slice(11, 12).alias("v4_from"),
    pl.col("lattice_max").str.slice(11, 12).alias("lat_to"),
    pl.col("v4_max").str.slice(11, 12).alias("v4_to"))
print("  distinct (lattice_start_hhmmss, v4_start_hhmmss) pairs, rounded to the minute:")
print(c.with_columns(pl.col("lat_from").str.slice(0, 5).alias("lat_from_hm"),
                     pl.col("v4_from").str.slice(0, 5).alias("v4_from_hm"))
       .group_by(["lat_from_hm", "v4_from_hm"]).len().sort("len", descending=True))
print("  distinct (lattice_end, v4_end) pairs, rounded to the minute:")
print(c.with_columns(pl.col("lat_to").str.slice(0, 5).alias("lat_to_hm"),
                     pl.col("v4_to").str.slice(0, 5).alias("v4_to_hm"))
       .group_by(["lat_to_hm", "v4_to_hm"]).len().sort("len", descending=True))
mismatch = c.filter(pl.col("v4_to").str.slice(0, 5) != pl.col("lat_to").str.slice(0, 5))
print(f"\n  days where the v4 in-window end minute differs from the lattice end minute: {mismatch.height}")
print(mismatch.select(["month", "date", "lattice_max", "v4_max", "v3_max"]).head(25))

print()
print("=" * 110)
print("PER-MONTH COUNTS — V4 join (cross-generation, the X4 deliverable)")
print("=" * 110)
m4 = pl.read_csv(OUT / "nq_mbo_diagnostic.csv")
for side in ["corrected", "contaminated"]:
    print(f"\n--- {side} ---")
    print(m4.filter(pl.col("side") == side)
            .pivot(on="month", index="class", values="strict_count")
            .rename({m: m + "_strict" for m in MONTHS}))
    print(m4.filter(pl.col("side") == side)
            .pivot(on="month", index="class", values="equal_count")
            .rename({m: m + "_equal" for m in MONTHS}))
print("\nrows per month/side:")
print(m4.group_by(["side", "month"]).agg(pl.col("rows").first()).sort(["side", "month"]))

print()
print("=" * 110)
print("PER-MONTH COUNTS — V3 join (SAME generation as the lattice; supplementary)")
print("=" * 110)
m3 = pl.read_csv(OUT / "nq_mbo_v3_same_generation_map.csv")
for side in ["corrected", "contaminated"]:
    print(f"\n--- {side} ---")
    print(m3.filter(pl.col("side") == side)
            .pivot(on="month", index="class", values="strict_count"))
    print(m3.filter(pl.col("side") == side)
            .pivot(on="month", index="class", values="equal_count"))

print()
print("=" * 110)
print("V4-vs-V3 COUNT DIFFERENCE (same lattice, different event generation)")
print("=" * 110)
cmp = (m4.rename({"strict_count": "s4", "equal_count": "e4"})
         .join(m3.rename({"strict_count": "s3", "equal_count": "e3"}),
               on=["side", "month", "class", "boundary"], how="full", coalesce=True)
         .with_columns((pl.col("s4") - pl.col("s3")).alias("d_strict"),
                       (pl.col("e4") - pl.col("e3")).alias("d_equal"))
         .sort(["side", "month", "class"]))
print(cmp.select(["side", "month", "class", "s4", "s3", "d_strict", "e4", "e3", "d_equal"]))
cmp.write_csv(OUT / "v4_vs_v3_count_delta.csv")
