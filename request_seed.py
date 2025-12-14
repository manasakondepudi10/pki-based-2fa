import requests

STUDENT_ID = "23P31A4238"
REPO_URL = "https://github.com/manasakondepudi10/pki-based-2fa"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

with open("student_public.pem") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": REPO_URL,
    "public_key": public_key
}

res = requests.post(API_URL, json=payload, timeout=30)
res.raise_for_status()

encrypted_seed = res.json()["encrypted_seed"]

with open("encrypted_seed.txt", "w") as f:
    f.write(encrypted_seed)

print("Encrypted seed saved")
