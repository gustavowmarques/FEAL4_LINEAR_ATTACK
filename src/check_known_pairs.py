# src/check_known_pairs.py
from src.data import parse_known_file
if __name__ == "__main__":
    pairs = parse_known_file("known.txt")
    print(f"Loaded {len(pairs)} pairs.")
    for i,(pt,ct) in enumerate(pairs[:5]):
        print(i, "PT:", pt.hex(), "CT:", ct.hex())
