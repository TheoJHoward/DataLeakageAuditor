# One-cell recompute: a4_runner net_delta on zc v4_gapfill (2025-01)

- pandas 3.0.1, numpy 2.4.2, pyarrow 23.0.1, python 3.12.10
- source file (read-only): `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\v4_gapfill\zc_trades_tagged_2025-01.parquet`
- instrument: **zc** (preferred per a4_runner.py:134-140 -> ROOT/processed/zc/v4_gapfill); file exists, so no fallback to he/le needed

## (e) Loaded dtypes (execution witness)

| column | arrow type (parquet schema as read) | pandas dtype after .to_pandas() |
|---|---|---|
| ts_event | timestamp[ns, tz=UTC] | datetime64[ns, UTC] |
| price | double | float64 |
| size | uint32 | uint32 |
| is_buy_aggressor | bool | bool |

- rows in month file: 398,188; ts range 2025-01-02 14:30:00+00:00 .. 2025-01-31 19:19:59.714578065+00:00

## (b) Session-hour slice: 2025-01-02 14:30:00+00:00 .. 2025-01-02 15:30:00+00:00  (5,294 trades)

- signed_size dtype as executed: **uint32** (np.where(bool, uint32, -uint32) stays unsigned; negation wraps mod 2**32)
- groupby-sum net_delta dtype as executed: **uint64**

- as-intended signed_size dtype: int64; as-intended net_delta dtype: int64

## (c)/(d) The two windows, side by side

| window | second (UTC) | buys | sells | trades | as-executed raw (uint64) | as-executed float32 | as-intended (int64) | float32(2^32*sells) | raw == 2^32*sells + intended | f32_exec == f32(2^32*sells) | f32 diff |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A: >=1 buy and >=1 sell | 2025-01-02 14:53:12+00:00 | 17 | 17 | 34 | 73014445046 | np.float32(7.301444e+10) | 1014 | np.float32(7.301444e+10) | True | True | 0.0 |
| B: >=2 sells | 2025-01-02 14:30:01+00:00 | 40 | 61 | 101 | 261993004958 | np.float32(2.61993e+11) | -98 | np.float32(2.61993e+11) | True | True | 0.0 |

## Hour-wide census (all 1-second windows in the slice)

- windows: 1412; windows containing >=1 sell: 1080
- raw identity `as_executed == 2^32*sells + true_delta` holds in **1412/1412**
- strong form `float32(as_executed) == float32(2^32*sells)` holds in **1076/1412**
- strong-form violations: 336 -- largest |true delta| among them: 762; examples:
    - 2025-01-02 15:03:40+00:00: sells=4, true delta=-762, f32_exec=17179868160.0, f32_strong=17179869184.0, diff=-1024.0
    - 2025-01-02 15:10:39+00:00: sells=1, true delta=-136, f32_exec=4294967040.0, f32_strong=4294967296.0, diff=-256.0
    - 2025-01-02 15:16:28+00:00: sells=1, true delta=-179, f32_exec=4294967040.0, f32_strong=4294967296.0, diff=-256.0

## float32 spacing at 2^32 * k (measured, np.spacing)

| k (sell count) | value 2^32*k | np.spacing(float32(value)) | half-ulp (rounding radius) |
|---|---|---|---|
| 1 | 4294967296 | 512.0 | 256.0 |
| 2 | 8589934592 | 1024.0 | 512.0 |
| 3 | 12884901888 | 1024.0 | 512.0 |
| 5 | 21474836480 | 2048.0 | 1024.0 |
| 10 | 42949672960 | 4096.0 | 2048.0 |
| 50 | 214748364800 | 16384.0 | 8192.0 |
| 100 | 429496729600 | 32768.0 | 16384.0 |

Any true-delta term with |delta| < half-ulp is rounded away entirely by the line-655 float32 cast; |delta| >= half-ulp survives only as a multiple of the ulp.

- true net_delta over the hour: min=-954, max=1014, max |delta|=1014, 99th pct |delta|=369.9

## Verdict

**CONFIRMED** (with one measured nuance on the strong form).

1. **Raw identity is exact, not approximate.** `as_executed_uint64 == 2^32 * sell_count + true_net_delta`
   held in **1412/1412** one-second windows of the slice. The uint32 negation at a4_runner.py:307 wraps
   each sell to `2^32 - size`, and the groupby-sum (a4_runner.py:311-312) accumulates in uint64 with no
   further overflow, so the "~" in the claim is actually "=" before the cast.
2. **Strong form on the two required windows: exact.** Window A (17 buys / 17 sells, true delta +1014,
   the largest |true delta| in the hour) and window B (40 buys / 61 sells, true delta -98) both satisfy
   `np.float32(as_executed) == np.float32(2^32 * sell_count)` exactly (diff 0.0). At those magnitudes
   the float32 ulp is 8192 (k=17) and 32768 (k=61), so half-ulp rounding radii of 4096 and 16384 swallow
   the entire true-delta term.
3. **Strong form hour-wide: 1076/1412 (76.2%).** In the 336 violating windows the true-delta term does
   NOT survive as itself: it survives only quantized to a multiple of the local float32 ulp
   (observed diffs -256, -512, -1024; worst case true delta -762 stored as -1024 at k=4). One boundary
   nuance: just below 2^32 the binade ulp is 256 (vs 512 above), so a true delta as small as -136
   rounded to -256 rather than vanishing. Relative to the stored value (>= 4.29e9), the surviving
   remnant is <= ~2.4e-7 of magnitude - float32(net_delta) is, to within +/-2 ulp, a pure encoding of
   `2^32 * sell_count`.
4. **Downstream amplification (context, not recomputed here):** line 655 casts after the rolling sums
   (a4_runner.py:329-334) accumulate up to 60 seconds of these values, so k becomes the sell count of
   the whole rolling window and the ulp grows proportionally - the fraction of windows where any
   true-delta remnant survives shrinks further at 5s/10s/30s/60s horizons.

Conclusion: with the working boolean classifier, the executed `net_delta` features encode
(2^32 x sell-trade count) plus at most +/-2 ulp of quantization noise; the signed-volume signal the
feature was intended to carry is either exactly zeroed (76.2% of windows at 1s in this slice, more at
longer horizons) or reduced to ulp-quantized jitter. The stored feature is effectively a scaled
sell-trade counter, not signed volume.

