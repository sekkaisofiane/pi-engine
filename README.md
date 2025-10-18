# Pi Engine — BBP hex-jumps + tiled Chudnovsky on a €150 Intel N150 mini-PC

**Goal:** Reproducible computation of π on low-cost hardware with open-source code.  
**Cores:** **BBP** (hexadecimal jump at index *n*) + **tiled Chudnovsky** (decimal, disk-based, checkpointed).

## Target Hardware
Mini-PC ≈ €150 — Intel Twin Lake N150 (Intel N150, 16 GB RAM).  
Any x86_64 machine with 8–16 GB RAM is suitable.

## Demos
```bash
# Spot check (single hex digit)
python code/pi_engine.py bbp --index 1_000_000

# 1000 decimal digits (timed)
python code/pi_engine.py chud --digits 1000 --chunk 1000 --out runs/out/pi_1k.txt
```

## Reproducibility
- Record each run in `results/experiments.csv`.  
- Verify 10 positions using:
  ```bash
  python scripts/verifier.py START LENGTH
  ```
- Hash outputs:
  ```powershell
  Get-FileHash runs/out/pi_*.txt -Algorithm SHA256 | Tee-Object results/hashes.txt
  ```

## Limitations
- Not a Guinness record attempt. BBP operates in base 16 for spot verification.  
- Simple Chudnovsky implementation; for >10⁶ digits, install `gmpy2` and adjust `chunk` / `workers`.
