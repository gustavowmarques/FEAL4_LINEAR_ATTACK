# tests/test_data.py
from src.data import parse_known_file

def test_known_file_loads():
    pairs = parse_known_file("known.txt")
    assert len(pairs) >= 100  # expect 200 in provided file
    pt, ct = pairs[0]
    assert len(pt) == 8 and len(ct) == 8
