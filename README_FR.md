[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17388049.svg)](https://doi.org/10.5281/zenodo.17388049)
# Pi Engine: BBP hex-jumps + tiled Chudnovsky on a €150 Intel N150 mini-PC

But: calcul reproductible de π sur matériel low‑cost avec code open‑source.
Noyaux: **BBP** (saut hex au rang *n*) + **Chudnovsky tuilé** (décimal, disque, checkpoints).

## Matériel cible
Mini‑PC ≈ €150 : Intel Twin Lake N150 (Intel N150, 16 Go RAM). Toute machine x86_64 8–16 Go convient.

## Démos
```bash
# Vérif spot (hex digit)
python code/pi_engine.py bbp --index 1_000_000

# 1000 décimales (mesuré)
python code/pi_engine.py chud --digits 1000 --chunk 1000 --out runs/out/pi_1k.txt
```

## Reproductibilité
- Renseigner `results/experiments.csv` après chaque run.
- Vérifier 10 positions avec `scripts/verifier.py START LENGTH`.
- Hasher les sorties:
```powershell
Get-FileHash runs/out/pi_*.txt -Algorithm SHA256 | Tee-Object results/hashes.txt
```

## Limites
- Pas un record Guinness. BBP = base 16 pour vérif ponctuelle.
- Chudnovsky simple; pour >10^6 digits, installer `gmpy2` et régler `chunk`/`workers`.
