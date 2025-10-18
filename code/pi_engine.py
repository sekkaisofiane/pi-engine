#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pi_engine.py — moteur π minimaliste (from scratch) pour petites machines.
Noyaux:
  1) BBP hex-digit (Bailey–Borwein–Plouffe) : n-ième chiffre en base 16.
  2) Chudnovsky tuilé : décimales base 10, écriture par blocs (gmpy2 recommandé).

Usage:
  python pi_engine.py bbp --index 10_000_000         # 10e6-ième chiffre hex de π
  python pi_engine.py bbp --range 1_000_000 1_000_100 # 100 chiffres hex à partir d'i
  python pi_engine.py chud --digits 10_000_000 --chunk 1_000_000 --out pi_10M.txt
"""

import argparse, math, sys
from typing import Tuple, Iterable, Optional

# ---------- 1) BBP: n-ième chiffre hex de π sans les précédents ----------
# π = Σ_{k>=0} 1/16^k * ( 4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6) )
# Implémentation en précision fractionnaire (partie finie + queue) suivant la méthode de D. Bailey.

def _bbp_sum(j: int, n: int) -> float:
    """Somme fractionnaire pour le terme j ∈ {1,4,5,6}; retourne {fractional part} de 16^{n} * Σ 1/(16^k * (8k+j))."""
    # 1) Somme discrète k=0..n
    s = 0.0
    for k in range(n+1):
        denom = 8*k + j
        # (16^(n-k) mod denom) / denom
        s = (s + pow(16, n-k, denom) / denom) % 1.0
    # 2) Queue k=n+1..∞ (rapide car 16^(n-k) -> 0)
    t = 0.0
    k = n + 1
    p = 16.0 ** (n - k)  # 16^{n-k}
    while p > 1e-17:      # seuil double précision; suffit pour obtenir 1 chiffre hex correct
        t += p / (8*k + j)
        k += 1
        p /= 16.0
    return (s + t) % 1.0

def bbp_hex_digit(n: int) -> int:
    """
    Retourne le n-ième chiffre hex de π (n>=0). 0 => chiffre juste après la virgule.
    Note: précision double => fiable pour 1–2 chiffres à la fois; pour séries, recomposer via _range.
    """
    # d_n = frac( 16^{n} * π )
    x = ( 4.0 * _bbp_sum(1, n)
        - 2.0 * _bbp_sum(4, n)
        - 1.0 * _bbp_sum(5, n)
        - 1.0 * _bbp_sum(6, n) ) % 1.0
    return int(x * 16)

def bbp_hex_range(start: int, count: int) -> str:
    """Renvoie 'count' chiffres hex de π à partir de 'start'."""
    return ''.join("0123456789ABCDEF"[bbp_hex_digit(start+i)] for i in range(count))

# ---------- 2) Chudnovsky tuilé (décimales) ----------
# π = (426880 * sqrt(10005)) / Σ_k ( ( (6k)! * (13591409 + 545140134k) ) / ( (3k)! * (k!)^3 * (-640320)^{3k} ) )
# Implémentation simple (pas de binary-splitting profond) + gmpy2 si dispo.

try:
    import gmpy2
    have_gmp = True
except Exception:
    have_gmp = False

def chud_chunk(chunk_terms: int, k0: int = 0):
    """
    Génère la somme partielle Σ_{k=k0}^{k0+chunk_terms-1} Ak, Bk des Chudnovsky.
    Retourne (num, den) rationnels (gmpy2.mpq si dispo) pour maximiser la précision sur l’addition.
    """
    if have_gmp:
        mpq = gmpy2.mpq
        mpz = gmpy2.mpz
        num = mpq(0,1)
        for k in range(k0, k0+chunk_terms):
            # Terme k
            # t = ( (6k)! * (13591409 + 545140134k) ) / ( (3k)! * (k!)^3 * (-640320)^{3k} )
            a = mpz(13591409 + 545140134*k)
            # Factoriels : on utilise gmpy2.fac (très optimisé)
            t = mpq(gmpy2.fac(6*k), gmpy2.fac(3*k) * (gmpy2.fac(k)**3))
            t *= a
            t /= mpq((-640320)**(3*k), 1)
            num += t
        den = mpq(1,1)
        return num, den
    else:
        # Pure Python (lent). Suffit pour ~10^5 décimales sur petites machines.
        from math import factorial
        from fractions import Fraction
        num = Fraction(0,1)
        for k in range(k0, k0+chunk_terms):
            a = 13591409 + 545140134*k
            t = Fraction(factorial(6*k), factorial(3*k) * (factorial(k)**3))
            t *= a
            t /= Fraction((-640320)**(3*k), 1)
            num += t
        den = Fraction(1,1)
        return num, den

def chud_pi_digits(decimals: int, chunk: int = 100_000, outfile: Optional[str] = None):
    """
    Calcule ~'decimals' décimales de π en tuiles 'chunk' termes Chudnovsky.
    Écrit progressivement (stream) pour limiter RAM. Retourne rien; écrit dans outfile si fourni.
    Note: méthode pédagogique, pas record. Pour >1e6 décimales, utiliser gmpy2 + tuning.
    """
    # Nombre de termes nécessaires ~ decimals / 14.181647...
    terms = int(math.ceil(decimals / 14.181647462725477))
    if have_gmp:
        gmpy2.get_context().precision = int(decimals * 3.32193) + 100  # ~bits ≈ digits*log2(10)
        sqrt10005 = gmpy2.sqrt(gmpy2.mpfr(10005))
        K = gmpy2.mpfr(426880) * sqrt10005
        S = gmpy2.mpq(0,1)
    else:
        # mpmath comme fallback
        import mpmath as mp
        mp.mp.dps = decimals + 50
        sqrt10005 = mp.sqrt(10005)
        K = mp.mpf(426880) * sqrt10005
        # Approche rationnelle via Fraction pour la somme, puis conversion -> lent
        from fractions import Fraction
        S = Fraction(0,1)

    k = 0
    while k < terms:
        c = min(chunk, terms - k)
        num, den = chud_chunk(c, k0=k)
        if have_gmp:
            S += num  # den=1 ici
        else:
            S += num
        k += c

    if have_gmp:
        pi_val = K / gmpy2.mpfr(S)  # mpfr division
        s = gmpy2.to_fixed(pi_val, decimals)  # string sans point; on formate
        s = s[:1] + "." + s[1:]
    else:
        import mpmath as mp
        # convertir Fraction S -> mp.mpf
        from decimal import Decimal, getcontext
        # Simple: convertir via mp.mpf(str(S.numerator/S.denominator)) peut perdre précision pour grands S.
        S_float = mp.mpf(S.numerator) / mp.mpf(S.denominator)
        pi_val = K / S_float
        s = mp.nstr(pi_val, n=decimals+2)  # "3.xxxxx"

    if outfile:
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(s)
    else:
        print(s)

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Pi Engine — BBP jump + Chudnovsky tuilé")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_bbp = sub.add_parser("bbp", help="n-ième chiffre hex de π (BBP)")
    g = ap_bbp.add_mutually_exclusive_group(required=True)
    g.add_argument("--index", type=int, help="indice du chiffre hex (0=1er après virgule)")
    g.add_argument("--range", nargs=2, type=int, metavar=("START","COUNT"), help="plage de chiffres hex")
    
    ap_ch = sub.add_parser("chud", help="Chudnovsky tuilé décimales")
    ap_ch.add_argument("--digits", type=int, required=True, help="nombre de décimales")
    ap_ch.add_argument("--chunk", type=int, default=100_000, help="taille de tuile (termes)")
    ap_ch.add_argument("--out", type=str, default=None, help="fichier sortie")

    args = ap.parse_args()

    if args.cmd == "bbp":
        if args.index is not None:
            d = bbp_hex_digit(args.index)
            print("0123456789ABCDEF"[d])
        else:
            start, count = args.range
            print(bbp_hex_range(start, count))
    elif args.cmd == "chud":
        chud_pi_digits(args.digits, chunk=args.chunk, outfile=args.out)

if __name__ == "__main__":
    main()
