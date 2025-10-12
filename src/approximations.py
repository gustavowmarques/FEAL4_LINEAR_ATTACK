# src/approximations.py
# Put linear-mask / approximation functions here.
# Each mask function must take (pt_bytes, ct_bytes, candidate) and return 0/1
# - pt_bytes and ct_bytes are length-8 bytes objects
# - candidate is an integer (candidate subkey byte or candidate pair packed int)
#
# Start with a toy mask that does not require partial decryption so we can
# validate the full pipeline. Replace toy_mask with your real linear expression
# that uses partial decryption.

from typing import Tuple
from src.feal import pack32  # uses pack32/unpack32 semantics from feal.py

def toy_mask(pt: bytes, ct: bytes, candidate: int) -> int:
    """
    Example toy mask:
    parity(pt[0]) XOR parity(ct[0] XOR candidate)
    This is only to validate the pipeline and scoring.
    """
    b1 = bin(pt[0]).count("1") & 1
    b2 = bin(ct[0] ^ (candidate & 0xFF)).count("1") & 1
    return b1 ^ b2

# Template example for a real approximation:
# def real_mask_lastround_byte(pt: bytes, ct: bytes, candidate_bytes: Tuple[int,int]):
#     """
#     Example: candidate_bytes = (k4_byte_guess, k5_byte_guess)
#     You should implement partial decryption to compute the intermediate byte(s)
#     that your linear approximation uses, then return 0/1 parity.
#     """
#     k4_byte, k5_byte = candidate_bytes
#     # compute partial decryption using ct and these bytes...
#     # compute parity of selected bits / bytes of plaintext and partial state...
#     # return 0 or 1
#     raise NotImplementedError("Replace this with your partial-decrypt based mask.")
