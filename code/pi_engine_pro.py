#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pi_engine_pro.py — version "pro" du moteur π utilisant un binary splitting simplifié et le calcul tuilé en parallèle.

Cette implémentation s'inspire du moteur pédagogique dans pi_engine.py mais ajoute :
  * calcul par blocs en parallèle avec multiprocessing pour accélérer la sommation
  * points de contrôle (checkpoints) pour reprendre le calcul en cas d'interruption
  * écriture finale dans un fichier, sans stocker toute la chaîne en mémoire

Remarque : il ne s'agit pas d'un record Guinness ; c'est un outil de démonstration adapté à des machines modestes.
"""

import argparse
import json
import math
import os
from typing import Optional, Tuple, List

try:
    import gmpy2
    HAVE_GMP = True
except Exception:
    HAVE_GMP = False

# Importer chud_chunk depuis le moteur pédagogique. Ceci évite de dupliquer le code.
# Le module pi_engine.py doit se trouver dans le même répertoire que ce fichier.
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from pi_engine import chud_chunk, have_gmp as BASE_HAVE_GMP

# Pour éviter d'instancier de nouveaux objets dans chaque worker, on définit une
# fonction globale. La signature doit accepter un tuple d'arguments.

def _worker_task(args: Tuple[int, int]):
    """Fonction appelée en parallèle. Calcule la somme partielle sur chunk_terms termes à partir de k0."""
    chunk_terms, k0 = args
    return chud_chunk(chunk_terms, k0)


def load_checkpoint(path: str):
    """Charge un point de contrôle depuis un fichier JSON. Retourne (k_start, num, den)."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    k_start = data.get("k_start", 0)
    num_str = data.get("num")
    den_str = data.get("den")
    if num_str is None or den_str is None:
        raise ValueError("Checkpoint invalide : num ou den manquant")
    if HAVE_GMP:
        num = gmpy2.mpq(num_str)
        den = gmpy2.mpq(den_str)
        return k_start, num, den
    else:
        # convertir les chaînes en int puis fraction
        from fractions import Fraction
        num = Fraction(int(num_str))
        den = Fraction(int(den_str))
        return k_start, num, den


def save_checkpoint(path: str, k_start: int, num, den):
    """Sauvegarde un point de contrôle dans un fichier JSON. num et den doivent être convertibles en chaîne."""
    if HAVE_GMP:
        num_str = gmpy2.to_text(num)
        den_str = gmpy2.to_text(den)
    else:
        num_str = str(num.numerator)
        den_str = str(num.denominator)
    data = {
        "k_start": k_start,
        "num": num_str,
        "den": den_str,
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def compute_pi(decimals: int, workers: int = 1, chunk: int = 1000, checkpoint: Optional[str] = None, outfile: Optional[str] = None):
    """
    Calcule π avec précision décimale donnée à l'aide d'une somme Chudnovsky tuilée en parallèle.

    :param decimals: nombre de décimales désirées
    :param workers: nombre de processus parallèles utilisés
    :param chunk: nombre de termes Chudnovsky par bloc
    :param checkpoint: chemin du fichier de point de contrôle (optionnel)
    :param outfile: chemin du fichier de sortie (optionnel)
    """
    # Nombre de termes nécessaires ~ decimals / 14.181647...
    terms = int(math.ceil(decimals / 14.181647462725477))

    # Charger un checkpoint existant si spécifié
    k_start = 0
    # S représente la somme partielle (numérateur). den est toujours 1 avec cette implémentation.
    if checkpoint and os.path.exists(checkpoint):
        try:
            k_start_loaded, num_loaded, den_loaded = load_checkpoint(checkpoint)
            k_start = k_start_loaded
            S = num_loaded  # numérateur
            # den_loaded devrait être 1 dans la version actuelle
            den = den_loaded
            print(f"Checkpoint chargé : reprise à k={k_start}.")
        except Exception as e:
            print(f"Impossible de charger le checkpoint: {e}. Recalcul depuis zéro.")
            S = None
    else:
        S = None

    if S is None:
        # Initialiser la somme partielle
        if HAVE_GMP:
            S = gmpy2.mpq(0, 1)
        else:
            from fractions import Fraction
            S = Fraction(0, 1)

    # Préparer le pool de processus
    workers = max(1, workers)
    # Créer un pool seulement si workers > 1
    pool = None
    if workers > 1:
        try:
            from multiprocessing import Pool
            pool = Pool(processes=workers)
        except Exception as e:
            print(f"Impossible de créer un pool de {workers} travailleurs : {e}. Utilisation d'un seul processus.")
            pool = None
            workers = 1

    # Somme en blocs jusqu'à atteindre le nombre total de termes
    k = k_start
    while k < terms:
        # Déterminer le nombre de blocs à calculer lors de cette itération
        # On lance au plus 'workers' tâches à la fois
        tasks: List[Tuple[int, int]] = []
        for _ in range(workers):
            if k >= terms:
                break
            c = min(chunk, terms - k)
            tasks.append((c, k))
            k += c
        # Exécution des tâches
        if pool:
            results = pool.map(_worker_task, tasks)
        else:
            results = [_worker_task(t) for t in tasks]
        # Agrégation des résultats
        for (num_part, den_part) in results:
            # den_part devrait toujours être 1 pour gmpy2.mpq; sinon Fraction
            if HAVE_GMP:
                S += num_part
            else:
                S += num_part
        # Sauvegarder le point de contrôle après ce lot si demandé
        if checkpoint:
            try:
                # den est toujours 1 => utiliser 1
                den_val = 1
                save_checkpoint(checkpoint, k, S, den_val)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du checkpoint: {e}")

    # Fermer le pool si créé
    if pool:
        pool.close()
        pool.join()

    # Calcul final de π : π = K / S où K = 426880 * sqrt(10005)
    if HAVE_GMP:
        gmpy2.get_context().precision = int(decimals * 3.32193) + 100
        sqrt10005 = gmpy2.sqrt(gmpy2.mpfr(10005))
        K = gmpy2.mpfr(426880) * sqrt10005
        pi_val = K / gmpy2.mpfr(S)
        s = gmpy2.to_fixed(pi_val, decimals)
        s = s[:1] + "." + s[1:]
    else:
        import mpmath as mp
        mp.mp.dps = decimals + 50
        sqrt10005 = mp.sqrt(10005)
        K = mp.mpf(426880) * sqrt10005
        # S est Fraction => convertir en mp.mpf pour division
        from decimal import Decimal, getcontext
        S_float = mp.mpf(S.numerator) / mp.mpf(S.denominator)
        pi_val = K / S_float
        s = mp.nstr(pi_val, n=decimals+2)

    # Écrire le résultat
    if outfile:
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(s)
    else:
        print(s)


def main():
    parser = argparse.ArgumentParser(description="Pi Engine Pro — Chudnovsky parallèle avec checkpoints")
    parser.add_argument("--digits", type=int, required=True, help="nombre de décimales à calculer")
    parser.add_argument("--workers", type=int, default=1, help="nombre de processus parallèles")
    parser.add_argument("--chunk", type=int, default=1000, help="taille de tuile (termes) par tâche")
    parser.add_argument("--checkpoint", type=str, default=None, help="fichier checkpoint pour reprendre le calcul")
    parser.add_argument("--out", type=str, default=None, help="fichier de sortie pour écrire les décimales de π")

    args = parser.parse_args()
    compute_pi(decimals=args.digits, workers=args.workers, chunk=args.chunk, checkpoint=args.checkpoint, outfile=args.out)


if __name__ == "__main__":
    main()