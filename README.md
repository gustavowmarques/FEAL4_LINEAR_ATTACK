# Linear Cryptanalysis of FEAL-4 (Java)

This repository contains my MSc cryptography assignment: a full **linear cryptanalysis attack** against the **FEAL-4** 64-bit block cipher, implemented in **Java**.

The objective of the project was to recover as many bits as possible of the six **32-bit subkeys (K0…K5)** used in FEAL-4 encryption, using a dataset of known plaintext–ciphertext pairs.

> Academic / portfolio note: This is an educational cryptanalysis implementation for a known weak cipher (FEAL). It is **not** intended for misuse.

---

## Project overview

- Cipher: **FEAL-4** (Feistel structure, 64-bit block)
- Technique: **Linear cryptanalysis** (Matsui-style linear approximations)
- Dataset: `known.txt` containing **200 known plaintext–ciphertext pairs**
- Implementation language: **Java**
- Outcome: Successful recovery of a verified key set producing correct ciphertexts for the full dataset.

---

## Verified results (one valid key set)

Due to FEAL’s weak key symmetry, the attack can produce multiple equivalent key sets. One verified set is:

| Subkey | 32-bit Hex |
|------:|------------|
| K0 | 63cab942 |
| K1 | 00a0c541 |
| K2 | c6f4095a |
| K3 | 66204c03 |
| K4 | 4b37d10a |
| K5 | d2a24877 |

Verification output (via `Verifier`):
- Loaded 200 pairs
- All pairs matched (verified)

See `JavaCodeResult.txt` for additional valid combinations found.

---

## Repository contents

- `FEAL.java` — Reference FEAL implementation (encryption/decryption)
- `MyFealLinear.java` — Main linear cryptanalysis / key recovery logic
- `Verifier.java` — Verifies a candidate key set against `known.txt`
- `TestK4Mapping.java` — Helper/testing logic used during development
- `known.txt` — Known plaintext–ciphertext dataset (200 pairs)
- `JavaCodeResult.txt` — Output log / discovered key combinations
- `report/report.docx` — Assignment report describing theory + approach + results

---

## How to build and run

### Requirements
- Java JDK 8+ (recommended: JDK 11 or newer)

### Compile
From the repo root:

```bash
javac *.java
