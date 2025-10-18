# Release Notes v0.1.0

## Summary
Initial release of Pi Engine, a low-cost π computation tool using BBP and Chudnovsky algorithms on mini-PC hardware.

## New Features
- BBP hex-digit computation for spot verification.
- Tiled Chudnovsky decimal computation with disk streaming.
- Parallel processing support in pro version.
- Checkpointing for resumable computations.
- Verification scripts for BBP checks.
- Reproducible experiments with CSV logging.

## Performance
- Tested on Intel Twin Lake N150 (Intel N150, 16 GB RAM).
- R001: 1000 digits in 0.5s (2000 digits/s, 50 MB RAM).
- BBP checks: 10/10 OK for executed runs.

## Files
- Code: `pi_engine.py`, `pi_engine_pro.py`, `verifier.py`.
- Data: `experiments.csv`, `hashes.txt`.
- Paper: `paper.md` (FR), `paper.en.md` (EN).
- Figures: ASCII placeholders + Python scripts for plots.
- Metadata: `CITATION.cff`, `ZENODO.json`.
- LICENSE added; pi_engine_pro CLI corrected.

## Known Issues
- gmpy2 not installed; fallback to mpmath/Fraction.

## Future Work
- Install gmpy2 for faster computations.
- Complete full matrix of experiments.
- Add PDF generation from Markdown.
