# src/feal.py
# FEAL-4 reference implementation in Python (matches semantics of FEAL.c)
from typing import List

def pack32(b: bytes) -> int:
    """Pack 4 bytes into 32-bit word exactly like FEAL.c: b[0] is most-significant."""
    assert len(b) == 4
    return (b[3]) | (b[2] << 8) | (b[1] << 16) | (b[0] << 24)

def unpack32(a: int) -> bytes:
    """Unpack 32-bit word into 4 bytes matching pack32."""
    return bytes(((a >> 24) & 0xff, (a >> 16) & 0xff, (a >> 8) & 0xff, a & 0xff))

def rot2(x: int) -> int:
    """Rotate left by 2 bits for a byte (8-bit)."""
    x &= 0xff
    return ((x << 2) & 0xff) | ((x >> 6) & 0x03)

def G0(a: int, b: int) -> int:
    return rot2((a + b) & 0xff)

def G1(a: int, b: int) -> int:
    return rot2((a + b + 1) & 0xff)

def f_word(input32: int) -> int:
    """FEAL f() on 32-bit word implemented as bytes and G0/G1 operations."""
    x = list(unpack32(input32))
    y = [0,0,0,0]
    # The classic order used in FEAL.c
    y[1] = G1(x[1] ^ x[0], x[2] ^ x[3])
    y[0] = G0(x[0], y[1])
    y[2] = G0(y[1], x[2] ^ x[3])
    y[3] = G1(y[2], x[3])
    return pack32(bytes(y))

def feal4_encrypt(block: bytes, key: List[int]) -> bytes:
    """Encrypt one 8-byte block with 6 32-bit subkeys K0..K5 (list of six ints)."""
    assert len(block) == 8
    assert len(key) == 6
    left = pack32(block[0:4])
    right = left ^ pack32(block[4:8])
    for i in range(4):  # 4 rounds
        temp = right
        right = left ^ f_word(right ^ key[i])
        left = temp
    # final whitening (as in FEAL.c)
    temp = left
    left = right ^ key[4]
    right = temp ^ right ^ key[5]
    return unpack32(left) + unpack32(right)

def feal4_decrypt(block: bytes, key: List[int]) -> bytes:
    """Decrypt one 8-byte FEAL-4 block with key list [K0..K5]."""
    assert len(block) == 8
    assert len(key) == 6
    # Reverse whitening
    right = pack32(block[0:4]) ^ key[4]
    left = right ^ pack32(block[4:8]) ^ key[5]
    for i in range(4):
        temp = left
        left = right ^ f_word(left ^ key[4 - 1 - i])  # reverse order
        right = temp
    right ^= left
    return unpack32(left) + unpack32(right)
