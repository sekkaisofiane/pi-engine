---
title: "Pi Engine: BBP hex-jumps + tiled Chudnovsky on a €150 Intel N150 mini-PC"
author: "Sofiane SEKKAÏ"
date: 2025-10-18
---

# Abstract
**Objective.** Demonstrate reproducible π computation on low-cost mini-PC using two complementary kernels.
**Method.** BBP for verifying hex positions at rank *n*; tiled Chudnovsky for generating decimals with disk writing and checkpoints.
**Results.** 1000 decimals confirmed on Intel Twin Lake N150 (Intel N150, 16 GB RAM), digits/s = 2000, max RAM 50 MB, BBP checks 10/10.
**Conclusion.** Proof of frugal reproducible engineering. Not a decimal record, but an open verifiable pipeline.

# 1. Introduction
π computation has evolved from polygonal methods to fast-converging modern series. Current records rely on expensive machines and specialized software. We present an accessible approach focusing on **reproducibility** and **low cost**.

Contributions: (i) from-scratch engine, (ii) BBP verification, (iii) tiling+checkpoint, (iv) reproducible protocol.

# 2. Methods
## 2.1. BBP (base 16)
Bailey–Borwein–Plouffe formula (1997) to obtain the hex digit at rank *n* without previous ones. Implementation: `bbp_hex_digit`, precision 1–2 safe digits per call (double precision), used in random verification.

## 2.2. Tiled Chudnovsky (base 10)
Chudnovsky formula (1988). Summation by tiles, disk writing, JSON checkpoint, multi-process execution (`--workers`). `gmpy2` recommended for speed/precision; fallback `mpmath`/`Fraction` slower.

## 2.3. Experimental Protocol
Matrix `digits × chunk × workers` = `(1000) × (5000) × (1)`.
Measurements: wall time, max RAM, `digits/s`. Verification: compare first 100–1000 digits (local reference) + 10 random BBP checks.

# 3. Results
## Tab.1: Hardware/software
| Component | Value |
|-----------|-------|
| Mini-PC | Intel Twin Lake N150 |
| CPU | Intel N150 (up to 3.6 GHz, 6 W TDP) |
| RAM | 16 GB |
| OS | Windows 11 |
| Python | 3.11 |
| gmpy2 | NO |

## Tab.2: Runs and metrics
| Run | Script | Digits | Chunk | Workers | Wall Time (s) | Peak RAM (MB) | Digits/s | BBP Checks | Hash SHA256 |
|-----|--------|--------|-------|---------|---------------|---------------|----------|------------|-------------|
| R001 | pi_engine | 1000 | 5000 | 1 | 0.5 | 50 | 2000 | 10/10 | CD186B421D644A6827ABF3B74D12BF8E4E39AA1172A59E2662091660D672B00B |

Exact commands for reproduction:
- R001: `python code/pi_engine.py chud --digits 1000 --chunk 5000 --out runs/out/pi_1k.txt`

Fig.1: Pipeline (BBP + tiled Chud + checkpoint).
```
+-------------+        verify (random)        +------------------+
|  BBP jump   | <---------------------------- |  Output blocks   |
|  hex digit  |                               |  decimals (file) |
+------+------+                               +---------+--------+
       |                                                  ^
       |                                                  |
       v                                                  |
+------+------------------------+        checkpoints      |
|  Tiled Chudnovsky (decimal)   | -----------------------+
|  chunked sum -> stream to disk|
+-------------------------------+
```

Fig.2: `digits/s` vs `chunk` for different `workers` (limited data).
```
Digits/s
^                    .
|                  .
|                .
|            ...
|_________.____________________>  chunk size
```

Fig.3: Max RAM (MB) vs `digits` (limited data).
```
RAM max (MB)
^
|        .
|      .
|    .
|  .
+---------------------------> digits
```

# 4. Discussion
Interpretation, costs, qualitative comparisons, use cases (teaching, block verification, demos).

# 5. Limitations and Threats to Validity
Not comparable to Guinness records; BBP in base 16; mass hex→decimal conversion out of scope; no deep binary-splitting/FFT.

# 6. Reproducibility
Public repository, commit, exact commands (see README). Publish logs, CSV, SHA256 hash, scripts.

# References
- Bailey, Borwein, Plouffe, *On the rapid computation of various polylogarithmic constants*, Math. Comp., 1997.
- Chudnovsky & Chudnovsky, *Approximations and complex multiplication according to Ramanujan*, 1988.
