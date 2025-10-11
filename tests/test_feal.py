# tests/test_feal.py
from src.feal import feal4_encrypt, feal4_decrypt

def test_roundtrip_zero_key():
    key = [0]*6
    pt = bytes.fromhex("0011223344556677")
    ct = feal4_encrypt(pt, key)
    pt2 = feal4_decrypt(ct, key)
    assert pt2 == pt

def test_roundtrip_nonzero_key():
    key = [0x01020304, 0x11121314, 0xA0A1A2A3, 0x0B0C0D0E, 0xFFFFFFFF, 0x12345678]
    pt = bytes(range(8))
    ct = feal4_encrypt(pt, key)
    pt2 = feal4_decrypt(ct, key)
    assert pt2 == pt
