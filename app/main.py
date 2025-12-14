from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
import time
import pyotp

app = FastAPI()

DATA_PATH = "/data/seed.txt"
PRIVATE_KEY_PATH = "student_private.pem"


# ---------- Helpers ----------

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_seed(encrypted_seed_b64: str) -> str:
    private_key = load_private_key()

    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = decrypted.decode("utf-8").strip()

    # validate seed
    if len(seed) != 64 or not all(c in "0123456789abcdef" for c in seed):
        raise ValueError("Invalid seed format")

    return seed


def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


def generate_totp(hex_seed: str):
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    remaining = 30 - int(time.time()) % 30
    return code, remaining


def verify_totp(hex_seed: str, code: str) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=1)


# ---------- API Models ----------

class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# ---------- API Endpoints ----------

@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptRequest):
    try:
        seed = decrypt_seed(req.encrypted_seed)
        os.makedirs("/data", exist_ok=True)

        with open(DATA_PATH, "w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(DATA_PATH) as f:
        seed = f.read().strip()

    code, remaining = generate_totp(seed)
    return {"code": code, "valid_for": remaining}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(DATA_PATH) as f:
        seed = f.read().strip()

    is_valid = verify_totp(seed, req.code)
    return {"valid": is_valid}
