# Résumé des expériences

## Méthodes
BBP pour vérifs ponctuelles. Chudnovsky tuilé pour produire des blocs décimaux. Journalisation standardisée.

## Résultats
- Meilleur digits/s: 2000 (pour 1000 digits, R001)
- Pic RAM max: 50 MB (pour 1000 digits, R001)
- Fichier le plus long: pi_1k.txt (taille ~1kB, hash CD186B421D644A6827ABF3B74D12BF8E4E39AA1172A59E2662091660D672B00B)
- Runs exécutés: R001 (1000 digits).

## Vérifications BBP
- Échantillons 10/10 OK pour les runs: R001

## Hash SHA256
- Voir `results/hashes.txt` (généré hors dépôt).

## Commandes de reproduction
- R001: python code/pi_engine.py chud --digits 1000 --chunk 5000 --out runs/out/pi_1k.txt
