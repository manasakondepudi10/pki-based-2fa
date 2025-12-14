import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# YOUR COMMIT HASH
COMMIT_HASH = "efaa56f4d7e0d2116b414195220f08b9f9e4181c"


def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def load_instructor_public_key():
    with open("instructor_public.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read())


def sign_commit_hash(commit_hash: str) -> bytes:
    private_key = load_private_key()
    return private_key.sign(
        commit_hash.encode("utf-8"),  # IMPORTANT: ASCII STRING
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


def encrypt_signature(signature: bytes) -> bytes:
    instructor_public_key = load_instructor_public_key()
    return instructor_public_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


if __name__ == "__main__":
    signature = sign_commit_hash(COMMIT_HASH)
    encrypted_signature = encrypt_signature(signature)
    b64_signature = base64.b64encode(encrypted_signature).decode("utf-8")

    print("\n===== SUBMISSION VALUES =====\n")
    print("Latest Commit:")
    print(COMMIT_HASH)
    print("\nEncrypted Commit Signature (BASE64, SINGLE LINE):")
    print(b64_signature)
