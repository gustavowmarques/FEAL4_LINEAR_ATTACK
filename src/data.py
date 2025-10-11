# src/data.py
from typing import List, Tuple

def parse_known_file(path: str) -> List[Tuple[bytes, bytes]]:
    pairs = []
    with open(path, 'r') as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    # Expect Plaintext=... then Ciphertext=...
    for i in range(0, len(lines), 2):
        if i+1 >= len(lines):
            break
        pt_line = lines[i]
        ct_line = lines[i+1]
        if not (pt_line.startswith("Plaintext=") and ct_line.startswith("Ciphertext=")):
            raise ValueError(f"Unexpected format near lines {i}:{i+1}")
        pt_hex = pt_line.split('=',1)[1].strip()
        ct_hex = ct_line.split('=',1)[1].strip()
        pairs.append((bytes.fromhex(pt_hex), bytes.fromhex(ct_hex)))
    return pairs
