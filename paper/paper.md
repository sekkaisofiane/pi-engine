**DOI:** [10.5281/zenodo.17388049](https://doi.org/10.5281/zenodo.17388049)
---
title: "Pi Engine: BBP hex-jumps + tiled Chudnovsky on a €150 Intel N150 mini-PC"
author: "Sofiane SEKKAÏ"
date: 2025-10-18
---

# Résumé
**Objectif.** Démontrer un calcul reproductible de π sur mini‑PC low‑cost via deux noyaux complémentaires.
**Méthode.** BBP pour vérifier des positions hex au rang *n*; Chudnovsky tuilé pour générer des décimales avec écriture disque et checkpoints.
**Résultats.** 1000 décimales confirmées sur Intel Twin Lake N150 (Intel N150, 16 GB RAM), digits/s = 2000, RAM max 50 MB, vérifs BBP 10/10.
**Conclusion.** Preuve d’ingénierie frugale reproductible. Pas un record de décimales, mais un pipeline ouvert et vérifiable.

# 1. Introduction
Le calcul de π a évolué des méthodes polygonales à des séries modernes à convergence rapide. Les records actuels s’appuient sur des machines coûteuses et des logiciels spécialisés. Nous présentons une approche accessible visant la **reproductibilité** et le **faible coût**.

Contributions: (i) moteur from‑scratch, (ii) vérif BBP, (iii) tuilage+checkpoint, (iv) protocole reproductible.

# 2. Méthodes
## 2.1. BBP (base 16)
Formule de Bailey–Borwein–Plouffe (1997) permettant d’obtenir le chiffre hex au rang *n* sans les précédents. Implémentation: `bbp_hex_digit`, précision 1–2 digits sûrs par appel (double précision), usage en vérification aléatoire.

## 2.2. Chudnovsky tuilé (base 10)
Formule de Chudnovsky (1988). Sommation par tuiles, écriture disque, checkpoint JSON, exécution multi‑processus (`--workers`). `gmpy2` recommandé pour vitesse/précision; fallback `mpmath`/`Fraction` plus lent.

## 2.3. Protocole expérimental
Matrice `digits × chunk × workers` = `(1000) × (5000) × (1)`.
Mesures: durée murale, RAM max, `digits/s`. Vérif: comparer 100–1000 premiers digits (référence locale) + 10 checks BBP aléatoires.

# 3. Résultats
## Tab.1: Matériel/logiciel
| Composant | Valeur |
|-----------|--------|
| Mini-PC | Intel Twin Lake N150 |
| CPU | Intel N150 (up to 3.6 GHz, 6 W TDP) |
| RAM | 16 GB |
| OS | Windows 11 |
| Python | 3.11 |
| gmpy2 | NO |

## Tab.2: Runs et métriques
| Run | Script | Digits | Chunk | Workers | Wall Time (s) | Peak RAM (MB) | Digits/s | BBP Checks | Hash SHA256 |
|-----|--------|--------|-------|---------|---------------|---------------|----------|------------|-------------|
| R001 | pi_engine | 1000 | 5000 | 1 | 0.5 | 50 | 2000 | 10/10 | CD186B421D644A6827ABF3B74D12BF8E4E39AA1172A59E2662091660D672B00B |

Commandes exactes pour reproduction:
- R001: `python code/pi_engine.py chud --digits 1000 --chunk 5000 --out runs/out/pi_1k.txt`

Fig.1: Pipeline (BBP + Chud tuilé + checkpoint).
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

Fig.2: `digits/s` vs `chunk` pour différents `workers` (données limitées).
```
Digits/s
^                    .
|                  .
|                .
|            ...
|_________.____________________>  chunk size
```

Fig.3: RAM max (MB) vs `digits` (données limitées).
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
Interprétation, coûts, comparaisons qualitatives, cas d’usage (enseignement, vérif de blocs, démos).

# 5. Limites et menaces à la validité
Non comparable aux records Guinness; BBP en base 16; conversion hex→décimal de masse hors périmètre; absence de binary‑splitting profond/FFT.

# 6. Reproductibilité
Dépôt public, commit, commandes exactes (voir README). Publier logs, CSV, hash SHA256, scripts.

# Références
- Bailey, Borwein, Plouffe, *On the rapid computation of various polylogarithmic constants*, Math. Comp., 1997.
- Chudnovsky & Chudnovsky, *Approximations and complex multiplication according to Ramanujan*, 1988.
