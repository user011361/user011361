#!/usr/bin/env python3
"""Generate random string with specified MD5 first byte and save to file."""
from __future__ import annotations

import argparse
import hashlib
import secrets
import string

ALPHABET: str = string.ascii_uppercase + string.digits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a random string whose MD5 hash starts with a specific byte."
    )
    parser.add_argument(
        "-n",
        "--length",
        type=int,
        default=10,
        help="Length of the random string (default: 10).",
    )
    parser.add_argument(
        "-m",
        "--md5-byte",
        type=str,
        default="0x00",
        help="Desired first byte of the MD5 hash in hex (default: 0x00).",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="randomfile.txt",
        help="Filename to store the resulting string (default: randomfile.txt).",
    )
    return parser.parse_args()


def sanitize_target(byte_str: str) -> int:
    byte_str = byte_str.strip().lower()
    if byte_str.startswith("0x"):
        byte_str = byte_str[2:]
    if not 1 <= len(byte_str) <= 2:
        raise ValueError("Target byte must be 1 or 2 hex characters long.")
    try:
        value = int(byte_str, 16)
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValueError("Target byte must be a valid hexadecimal value.") from exc
    if not 0 <= value <= 0xFF:
        raise ValueError("Target byte must be between 0x00 and 0xFF.")
    return value


def generate_candidate(length: int, alphabet: str) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main() -> None:
    args = parse_args()
    target_byte = sanitize_target(args.md5_byte)
    length = args.length
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    attempt = 0
    while True:
        attempt += 1
        candidate = generate_candidate(length, ALPHABET)
        digest = hashlib.md5(candidate.encode("ascii"))
        digest_bytes = digest.digest()
        if digest_bytes[0] == target_byte:
            digest_hex = digest.hexdigest()
            with open(args.file, "w", encoding="utf-8") as file_handle:
                file_handle.write(candidate)
            print(f"[+] Got in {attempt} : {digest_hex}\n{candidate}")
            break


if __name__ == "__main__":
    main()
