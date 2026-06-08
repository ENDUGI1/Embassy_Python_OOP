"""
Utilitas keamanan password.

Memakai PBKDF2-HMAC-SHA256 dari modul bawaan `hashlib` (tanpa dependency
tambahan) sehingga mudah dijalankan di mana saja, termasuk saat deploy.

Format hash yang disimpan:  pbkdf2_sha256$<iterasi>$<salt_hex>$<digest_hex>
"""

import hashlib
import secrets

ALGO = "pbkdf2_sha256"
ITERATIONS = 100_000


def hash_password(plain: str) -> str:
    """Ubah password polos menjadi hash satu arah yang aman disimpan."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", plain.encode(), bytes.fromhex(salt), ITERATIONS
    ).hex()
    return f"{ALGO}${ITERATIONS}${salt}${digest}"


def verify_password(stored: str, plain: str) -> bool:
    """
    Cocokkan password input dengan nilai tersimpan.

    Mendukung dua bentuk:
      - Hash PBKDF2 (format di atas) — jalur normal.
      - Plaintext lama (data warisan dari versi CSV) — agar akun lama tetap bisa
        login sebelum sempat di-hash ulang.
    """
    if stored.startswith(ALGO + "$"):
        try:
            _, iterasi, salt, digest = stored.split("$")
            uji = hashlib.pbkdf2_hmac(
                "sha256", plain.encode(), bytes.fromhex(salt), int(iterasi)
            ).hex()
            return secrets.compare_digest(uji, digest)
        except (ValueError, TypeError):
            return False
    # Data warisan: bandingkan langsung (akan otomatis di-hash saat login sukses).
    return secrets.compare_digest(stored, plain)


def is_hashed(stored: str) -> bool:
    """True jika nilai sudah dalam bentuk hash, bukan plaintext."""
    return stored.startswith(ALGO + "$")
