# C5 — Wrap decidability from records alone: evidence log

Date of examination: 2026-08-11. Archive: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only; reads and hashes only).
Question: do archived records pin the ORIGINAL Phase 5 environment's pandas/numpy versions, and is the net_delta
subtraction site's dtype behavior under those versions decidable from records alone?

No installs, no venvs, no execution of old library versions were performed. The only code executed was the
current PATH python used to read parquet file METADATA (schema) — flagged below where used.

---

## 1. Version records found in the archive

### 1.1 requirements.txt (two byte-identical copies) — PRESCRIPTIVE, for the second computer
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\transfer\requirements.txt`
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\transfer\requirements.txt`
- mtime (both): 2026-04-07 08:25:20 — inside the Phase 5 run window (2026-04-05..08)
- sha256 (both): `3DF62D42E05036479EBCEC29028AD579A89668F29D4AD6F3280AF7811C54DC9A` (149 bytes)
- Verbatim content (complete):
  ```
  pandas==2.1.4
  numpy==1.26.4
  pyarrow==14.0.2
  lightgbm==4.3.0
  xgboost==2.0.3
  scikit-learn==1.4.0
  torch==2.1.2
  scipy==1.12.0
  tqdm==4.66.2
  psutil==5.9.8
  ```
- Context: sibling file `pc2_transfer\transfer\CLAUDE_CODE_START_HERE.md` (mtime 2026-04-07 08:43:03) is titled
  "SECOND COMPUTER SETUP / For Claude Code to execute autonomously". Its STEP 2: "Check: `python --version` /
  Need 3.10.x or 3.11.x or 3.12.x. / If missing, download Python 3.11 from python.org." STEP 3:
  "`pip install -r requirements.txt` / All versions pinned. Do not modify."
- Interpretation constraint (fact, not inference): this file PRESCRIBES an install for a second computer. No
  archived record shows this requirements set was ever installed on ANY machine (no pip log, no
  "Successfully installed" string anywhere in the archive — see §4).

### 1.2 PC2_SETUP_README.txt — PC1 environment frozen 2026-04-17 (hand-written record, git-tracked)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\PC2_TRANSFER_v4\PC2_SETUP_README.txt`, mtime 2026-04-17 08:09:10
- Git: the ONLY env-related file tracked by the archive repo (`git ls-files` filtered on
  requirement/environment/setup/readme/env); committed in `2e75345 2026-04-17 08:10 "A4 prep: PC2 transfer
  package manifest + pilot + work split"`.
- Verbatim (lines 42-59):
  ```
  PC1's environment (frozen at package time):

      Python 3.12.10
      OS: Windows-11-10.0.26200-SP0

      databento     == 0.70.0
      joblib        == 1.5.3
      lightgbm      == 4.6.0
      matplotlib    == 3.10.8
      numpy         == 2.4.2
      pandas        == 3.0.1
      psutil        == 7.2.2
      pyarrow       == 23.0.1
      requests      == 2.32.5
      scikit-learn  == 1.8.0
      scipy         == 1.17.1
      torch         == 2.6.0+cu124
      xgboost       == 3.2.0
  ```

### 1.3 pilot_results_pc1.json / pilot_results.json — MACHINE-GENERATED env record, 2026-04-17
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\PC2_TRANSFER_v4\pilot\pilot_results_pc1.json` (mtime 2026-04-17 08:07:09)
  and `pilot_results.json` (mtime 2026-04-17 08:07:01); both 24,296 bytes, identical `generated_utc`.
- Producer: `pilot_run.py` line 267 records `"python": sys.version.split()[0]` (plus platform/node/lib versions).
- Verbatim env block (identical in both files):
  ```
  "generated_utc": "2026-04-17T15:07:01.149445+00:00"
  "env": {"python": "3.12.10", "platform": "Windows-11-10.0.26200-SP0", "node": "VENGEANCE",
          "numpy": "2.4.2", "pandas": "3.0.1", "pyarrow": "unknown", "lightgbm": "4.6.0"}
  ```
- This is the only machine-generated interpreter/library version record anywhere in the archive. It postdates
  the Phase 5 runs by 9 days. Node name "VENGEANCE" appears nowhere else in the archive.

### 1.4 Phase 5 pre-fix launchers — interpreter pinned by path
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\run_phase5_batchA.bat` (and every other
  phase5 bat: run_phase5_batchB/cl/gc/nq/nq_30_60, run_dl_rerun_A/B, run_audit — all identical in form):
  ```
  set PYTHON="C:\Users\ttbea\AppData\Local\Programs\Python\Python312\python.exe"
  set LOG="C:\MBO_data\phase5_batchA.log"
  %PYTHON% -S -u "C:\MBO_data\phase5_ml.py" batchA < NUL >> %LOG% 2>&1
  ```
  Header comment: "REM Phase 5 batchA launcher (instruments group A) — last confirmed working 2026-04-04".
- So the pre-fix runs were launched with a SPECIFIC interpreter install dir (Python312) and `-S`.
- Run logs were written to `C:\MBO_data\*.log` — that drive is gone; NO copy of any phase5_batch*.log exists in
  the archive (Glob `**/phase5_batch*.log` = no files).

### 1.5 phase5_ml.py — pins the package source directory and the machine
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py`
  (byte-verified vs mirrors per prior items; header comment "last confirmed working 2026-04-05").
- Lines 5-8 (compensates the `-S` flag; forces imports from the interpreter's OWN site-packages):
  ```python
  import sys, os
  _sp = os.path.join(sys.prefix, "Lib", "site-packages")
  if _sp not in sys.path:
      sys.path.insert(0, _sp)
  ```
  With the launcher above, `sys.prefix` = `C:\Users\ttbea\AppData\Local\Programs\Python\Python312`, so the
  package source is pinned to `...\Python312\Lib\site-packages`.
- Lines 38-40:
  ```python
  PROJECT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
  PROC = PROJECT / "processed"
  LOCAL_DATA = Path(r"C:\MBO_data")
  ```
- Lines 105-106 (data dir resolution): `local = LOCAL_DATA / sym` / `return local if local.exists() else PROC / sym`
- Line 225: `trades = pq.read_table(str(tp)).to_pandas()`  (pyarrow.parquet read path)
- Lines 231-233 (the site):
  ```python
  is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \
           else trades["side"].isin(["B","Buy","buy"])
  trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])
  ```
- Lines 237-238, 253: `net_delta=("signed_vol","sum")` in a `groupby("ts_floor").agg`, then
  `snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()`.

### 1.6 Machine attribution of the Phase 5 artifacts
- pre-fix (phase5_ml.py) artifacts: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\phase5\`
  — `phase5_ZC_results.csv` + `checkpoint_zc.json` mtime 2026-04-05 08:12:48, then ZS 08:30:54, HE 09:00:16,
  LE 09:36:08 — one sequential stream matching `BATCH_A = ["zc", "zs", "he", "le"]` (phase5_ml.py line 805).
  BATCH_A mixes "main PC" instruments (HE, LE) with "PC2" instruments (ZC, ZS) — i.e. the code's batch split is
  NOT the two-machine instrument split described in PC2_START_HERE.md; one machine ran the batch. phase5_ml.py
  hard-codes the PC1 project path (line 38) and C:\MBO_data (line 40).
- phase5_fixed artifacts: `pc2_transfer\results\phase5_fixed\` — all four track logs (gpu_track, gpu_track2,
  cpu_track, cpu_track2; mtimes 2026-04-07..08) print `Results: C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase5_fixed\...`
  and together cover ALL 8 instruments x all 6 architectures on that one path. gpu_track2 (LSTM/CNN/Transformer
  on NQ GC ZC ZS — contains the ZC CNN 5s runs) line 8 verbatim:
  `Results: C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase5_fixed\gpu_track2`.
  `launch_gpu_track2.bat` (same dir): `cd /d "C:\Users\ttbea\OneDrive\Desktop\MBO_2025"` then
  `python -u "scripts\phase5_fixed.py" full ... --instruments NQ GC ZC ZS ...` (bare `python`, waits on local
  PID 53848 — a same-machine dependency).
- `results\pc2_all_phases\phase5_fixed\gpu_track2_log.txt` is a COPY of the same PC1 run (identical Results
  path); `results\phase5_fixed\`, `USB_ALL_PHASES\phase5_fixed\` likewise carry the same launch bat.
- Conclusion supported by these records: BOTH the pre-fix Phase 5 ZC runs and the phase5_fixed ZC runs were
  produced on the machine whose project root is `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` — "PC1"/"main PC" in
  the docs, node "VENGEANCE" per §1.3. PC2_START_HERE.md's PC1/PC2 split describes an intent (v4-era A4 split
  was real, per PC2_TRANSFER_v4), but no Phase 5 artifact in the archive traces to any non-PC1 machine.

### 1.7 Data identity: checksum manifest from inside the run window
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\transfer\checksums.txt` (96 lines, mtime 2026-04-07 08:33:03):
  ```
  ea2eee6136896b5f8a5b7ddc052f589c  data/zc/zc_snapshots_2025-01.parquet
  a2ccce4d3e69c001cd45a44b5eaf7eae  data/zc/zc_trades_tagged_2025-01.parquet
  ```
- Measured today (Get-FileHash MD5 of the archive files):
  - `processed\zc\zc_snapshots_2025-01.parquet`  md5 `ea2eee6136896b5f8a5b7ddc052f589c`, mtime 2026-04-02 14:31:53, 15,919,599 bytes — MATCH
  - `processed\zc\zc_trades_tagged_2025-01.parquet` md5 `a2ccce4d3e69c001cd45a44b5eaf7eae`, mtime 2026-04-02 14:31:53, 11,521,206 bytes — MATCH
- So the parquets the f2 rebuild read (the archive files) are byte-identical to the files hashed on 2026-04-07,
  and their mtimes predate the run window. Caveat: whether `C:\MBO_data\zc\` held byte-identical copies during
  the runs is NOT directly recorded (phase5_ml.py line 105-106 prefers C:\MBO_data if present; that drive's
  contents are gone). The manifest ties the transfer staging copy, not C:\MBO_data, to these bytes.

### 1.8 Parquet stored type of the operand (read from file metadata, current PATH python)
- `processed\zc\zc_trades_tagged_2025-01.parquet`, read via `pyarrow.parquet.ParquetFile` metadata only
  (current PATH python 3.12.10, pyarrow 23.0.1 — the Python312 install itself):
  - `size`: parquet physical=INT32, logical=`Int(bitWidth=32, isSigned=false)`; arrow type `uint32`, nullable=True
  - `aggressor_side`: physical=BYTE_ARRAY, logical=String; arrow `large_string`
  - `is_buy_aggressor`: arrow `bool`
  - num_rows = 397,457 (matches the C-item raw count)

---

## 2. Live-system corroboration (OUTSIDE the archive; read-only; the launcher names this directory)

The pre-fix launcher (§1.4) names `C:\Users\ttbea\AppData\Local\Programs\Python\Python312\python.exe` and
phase5_ml.py (§1.5) pins imports to that install's site-packages. Read-only inspection of that directory today:

- `python.exe` VersionInfo: ProductVersion 3.12.10, FileVersion 3.12.10 (file metadata; interpreter not executed
  for this). Install dir `Python312` CreationTime 2026-02-12 16:13:13.
- `Python312\Lib\site-packages` dist-info directories (Name / CreationTime / LastWriteTime):
  ```
  numpy-2.4.2.dist-info        2026-02-12 16:25:21 / 16:25:25
  pandas-3.0.1.dist-info       2026-02-18 18:11:10 / 18:11:26
  pyarrow-23.0.1.dist-info     2026-02-18 18:11:07 / 18:11:09
  scipy-1.17.1.dist-info       2026-03-02 11:06:19
  scikit_learn-1.8.0.dist-info 2026-03-02 20:13:55
  xgboost-3.2.0.dist-info      2026-03-29 20:36:48
  lightgbm-4.6.0.dist-info     2026-03-29 20:36:49
  torch-2.6.0+cu124.dist-info  2026-04-04 17:17:30
  ```
  All EIGHT match the 2026-04-17 frozen list (§1.2) exactly. All creation dates PRECEDE the Phase 5 window
  (torch on 2026-04-04, the day before the first run; header comment "last confirmed working 2026-04-04").
  No pandas-2.1.4 / numpy-1.26.4 / pyarrow-14.0.2 dist-info exists. A pip uninstall/reinstall or version swap
  after these dates would have produced later CreationTimes; none is later than 2026-04-04. Therefore, per this
  directory's own metadata, pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1 were continuously the installed versions
  in Python312 from 2026-02-18 (numpy: 02-12) through today — spanning 2026-04-05..08.
- The only other interpreter on the machine, `Python313` (created 2025-01-27), holds
  `numpy-2.4.2` / `pandas-3.0.0` / `pyarrow-23.0.0` (all created 2026-02-05) — also pandas 3.x / numpy 2.4.2;
  the requirements.txt versions exist NOWHERE on this machine.
- Bare `python` on PATH resolves today to `...\Python312\python.exe` (sys.prefix = Python312) — the interpreter
  the phase5_fixed bat would have picked up if PATH was the same in April (PATH state in April is not recorded;
  the 2026-04-17 pilot, run per README with bare `python`, reported 3.12.10, consistent).
- The current machine is Windows 11 build 10.0.26200 (session env), matching the recorded platform string
  `Windows-11-10.0.26200-SP0` (§1.2, §1.3): the machine examined IS PC1/VENGEANCE.

---

## 3. Decidability verdict

### Part 1 — Are the original versions pinned by records? YES (pinned), with the following structure:
- Archived records alone bracket, and effectively pin, PC1's environment: the 2026-04-17 machine-generated
  pilot env record and the 2026-04-17 hand-written frozen list (git-committed) both give
  **Python 3.12.10 / pandas 3.0.1 / numpy 2.4.2 (pyarrow 23.0.1 per the README; "unknown" in the pilot JSON)**
  on node VENGEANCE — 9 days after the runs; the launcher + phase5_ml.py pin the interpreter and package
  directory used by the runs; all Phase 5 ZC artifacts (pre-fix and phase5_fixed) attribute to PC1 by embedded
  paths and batch sequencing (§1.6). The lone conflicting record, requirements.txt (pandas 2.1.4/numpy 1.26.4),
  is a prescription for a second computer with no record of ever being installed, and its versions exist on no
  interpreter on PC1.
- The residual 9-day gap (no record dated 2026-04-05..08 itself; the C:\MBO_data run logs are lost) is closed by
  the read-only metadata of the very directory the archived launcher names (§2): dist-info creation dates show
  the pinned versions were laid down 2026-02-12..04-04 and never changed. Strictly archive-only, the pin is
  "bracketed + uncontradicted"; including the referenced install directory's metadata, the pin is continuous
  over the run window.
- PINNED: **pandas 3.0.1, numpy 2.4.2, pyarrow 23.0.1, Python 3.12.10, on PC1 ("VENGEANCE"), for both the
  pre-fix Phase 5 runs and the phase5_fixed runs (incl. ZC CNN 5s).** These are the SAME pandas/numpy versions
  as the f2 fixture rebuild environment (2026-08-09).

### Part 2 — Is the dtype outcome at the site decidable? DECIDABLE. Decided outcome: **the original Phase 5
runs wrapped modulo 2^32 at the signed_vol/net_delta site, identically to the f2 rebuild.**
Chain (each link a recorded/measured fact):
1. Input bytes identical: run-window MD5 manifest (2026-04-07) matches the archive ZC parquets the f2 rebuild
   read (§1.7). (Caveat: the C:\MBO_data copy itself is unrecorded; see blockers.)
2. Stored type of the operand: parquet logical UINT32 / arrow uint32 for `size` (§1.8) — a property of the file,
   not of any environment.
3. Materialization: pyarrow's documented Arrow→pandas mapping, "Arrow -> pandas Conversion" table:
   `(U)INT{8,16,32,64}` → `(u)int{8,16,32,64}` without nulls; `float64` only with nulls
   (https://arrow.apache.org/docs/python/pandas.html). The f2 rebuild measured `size` materializing as uint32
   from these same bytes; original pyarrow pinned at 23.0.1.
4. Code identical: phase5_ml.py byte-verified; the site is lines 231-233 → 237-238 → 253 (§1.5).
5. Version-identical execution witness: the f2 rebuild ran this site under pandas 3.0.1 / numpy 2.4.2 — exactly
   the pinned original versions — and the negation `-trades["size"]` on the uint32 Series wrapped modulo 2^32
   (recorded f2 finding). Same versions + same bytes + same code ⇒ same dtype outcome. No new execution needed.
6. Documentation support (cited, fetched 2026-08-11):
   - NumPy v2.4 Manual, "Data types" (https://numpy.org/doc/2.4/user/basics.types.html): "NumPy follows C
     casting rules, so that value would overflow and become 44 (300 - 256)"; "The fixed size of NumPy numeric
     types may cause overflow errors when a value requires more memory than available in the data type"
     (silent wrap illustrated with np.power int32 example). NOTE: the page does not contain an explicit
     sentence "unary negation of unsigned arrays wraps modulo 2^N" — documentation alone makes the wrap at the
     negation op strongly implied (C semantics) but not verbatim-quotable.
   - pyarrow pandas-integration doc as in link 3 above (explicit type table).
   Because of that NumPy-doc wording gap, the airtight decision rests on link 5 (the f2 execution under the
   pinned versions) rather than on changelog text alone. With link 5, the outcome is decided; by documentation
   strictly alone, it would be "decidable in all but the final negation wording", i.e. strongly implied but not
   quotable.

### Blockers / residual ambiguity (reported, not inferred away)
- No record dated 2026-04-05..08 states the versions directly; the pre-fix run logs lived on C:\MBO_data (gone).
  The pin is by bracketing records + the launcher-named directory's package metadata.
- Whether `C:\MBO_data\zc\` existed and was byte-identical to `processed\zc\` during the runs is unrecorded
  (phase5_ml.py line 105-106 falls back to `processed\` if the local dir is absent; either path yields the same
  bytes only if the local copy matched — the 2026-04-07 manifest covers the transfer staging copy, and the
  archive files match it).
- PATH contents on 2026-04-05..08 (for the bare-`python` phase5_fixed launcher) are unrecorded; today PATH
  resolves to Python312, and both interpreters on the machine carry pandas 3.x / numpy 2.4.2, so the outcome is
  invariant to this ambiguity.
- pilot JSON records pyarrow as "unknown" (pilot_run.py did not import it); pyarrow 23.0.1 rests on the README
  freeze + dist-info metadata.

---

## 4. Empty avenues (searched, nothing found)

- `environment*.yml`, `Pipfile`, `poetry.lock`, conda list dumps: Glob over the whole archive — none.
- pip freeze output anywhere: none. String `Successfully installed`: zero hits archive-wide
  (rg --no-ignore sweep; NOTE: `.gitignore` excludes `/pc2_transfer/`, `/results/`, `/transfer/`,
  `/USB_ALL_PHASES/` etc., so ignore-respecting greps silently miss most of the archive — all sweeps were
  re-run with --no-ignore).
- Version banners in run logs: none. `logs\` contains only v4-era g2/g3 reprocessing logs (2026-04-16..17);
  the four phase5_fixed track logs, checkpoint_phase5_fixed.json, master_phase5_fixed.csv, the pre-fix
  checkpoint_zc.json and phase5_ZC_results.csv contain NO version/env fields (schemas listed in session).
- Scripts that print versions: only `scripts\test_imports.py` (prints sys.version + lightgbm version), but no
  captured output of it exists anywhere in the archive.
- `docs\PROJECT_SUMMARY.md` (2026-04-04, day before runs): no python/pandas/numpy/environment/version content
  ("14,344 lines of Python" only). BOOKMAP_SETUP.md: generic `pip install bookmap numpy pandas` (no versions).
- MASTER_FINDINGS, USB_ALL_PHASES, live_sessions, paper, v4, v5: zero hits for
  `pandas==|numpy==|pyarrow==|pandas 3.|numpy 2.|pandas 2.|numpy 1.|VENGEANCE|Successfully installed`
  outside the files quoted above.
- Archive `.claude\`: only `launch.json` (a Bookmap dashboard launcher, quoted in session) and
  `settings.local.json` — no env records.
- Git history: repo starts 2026-04-15 (v4 era); only tracked env-related file is PC2_SETUP_README.txt
  (commit 2e75345, 2026-04-17 08:10). requirements.txt / transfer dirs are gitignored, never committed.
- Node name "VENGEANCE": appears only in the two pilot JSONs.
- No `*.log` copy of any C:\MBO_data phase5 log exists in the archive (Glob `**/phase5_batch*.log`: none).
