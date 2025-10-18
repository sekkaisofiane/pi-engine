import sys
sys.path.append('code')
from pi_engine import bbp_hex_digit

# Hex digits of π after the point: 2 4 3 F 6 A 8 8 8 5 A 3 ...
KNOWN = [0x2,0x4,0x3,0xF,0x6,0xA,0x8,0x8,0x8,0x5,0xA,0x3]
def test_bbp_hex_digit_prefix():
    for i, v in enumerate(KNOWN):
        assert bbp_hex_digit(i) == v

def test_bbp_hex_digit():
    # Known hex digits of pi (from execution)
    assert bbp_hex_digit(0) == 2  # 3.243F6A8885A3... but implementation starts from 0 as first after decimal
    assert bbp_hex_digit(1) == 4
    assert bbp_hex_digit(2) == 3
    assert bbp_hex_digit(3) == 15  # F
    assert bbp_hex_digit(4) == 6
    assert bbp_hex_digit(5) == 10  # A

if __name__ == "__main__":
    test_bbp_hex_digit()
