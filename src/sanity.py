# src/sanity.py
from src.feal import feal4_encrypt, feal4_decrypt
from src.data import parse_known_file

def sample_encrypt_decrypt():
    key = [0]*6
    pt = bytes.fromhex("0011223344556677")
    ct = feal4_encrypt(pt, key)
    print("PT:", pt.hex(), "CT:", ct.hex())
    print("Decrypt ->", feal4_decrypt(ct, key).hex())

if __name__ == "__main__":
    sample_encrypt_decrypt()
    pairs = parse_known_file("known.txt")
    print("First known pair:", pairs[0][0].hex(), pairs[0][1].hex())
