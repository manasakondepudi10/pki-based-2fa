import base64
import pyotp
from datetime import datetime, timezone
import os

DATA_PATH = "/data/seed.txt"

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


if not os.path.exists(DATA_PATH):
    print("Seed not found")
    exit(1)

with open(DATA_PATH) as f:
    hex_seed = f.read().strip()

base32_seed = hex_to_base32(hex_seed)
totp = pyotp.TOTP(base32_seed)

code = totp.now()
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

print(f"{timestamp} - 2FA Code: {code}")
