#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vérifie 10 positions hexadécimales aléatoires via BBP dans une plage donnée.
# Usage: python scripts/verifier.py START LENGTH

import sys, random
sys.path.append("code")
from pi_engine import bbp_hex_digit

def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/verifier.py START LENGTH")
        sys.exit(1)
    start = int(sys.argv[1])
    length = int(sys.argv[2])
    ok = 0
    for _ in range(10):
        i = random.randint(start, start + length - 1)
        try:
            d = bbp_hex_digit(i)
            if isinstance(d, int) and 0 <= d <= 15:
                print(f"{i}\t{hex(d)}")
                ok += 1
            else:
                print(f"{i}\tINVALID")
        except Exception as e:
            print(f"{i}\tERROR: {e}", file=sys.stderr)
    print(f"Checks: {ok}/10")
    sys.exit(0 if ok == 10 else 1)

if __name__ == "__main__":
    main()
