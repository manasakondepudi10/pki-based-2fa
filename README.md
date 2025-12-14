\# PKI-Based 2FA Authentication Microservice



\## Overview

This project implements a secure, containerized authentication microservice using Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) based two-factor authentication. It demonstrates real-world security practices such as RSA cryptography, TOTP verification, Docker containerization, cron jobs, and persistent storage.



The service decrypts a secure seed using RSA, generates TOTP codes, verifies user-provided codes, and periodically logs TOTP values using a cron job.



---



\## Features

\- RSA 4096-bit key–based seed decryption (OAEP with SHA-256)

\- TOTP-based 2FA (SHA-1, 30-second window, 6-digit codes)

\- REST API with three endpoints

\- Cron job running every minute to log TOTP codes

\- Dockerized using a multi-stage build

\- Persistent storage using Docker volumes

\- UTC timezone enforced across API and cron jobs



---



\## API Endpoints



\### POST `/decrypt-seed`

Decrypts the encrypted seed using the student private key and stores it persistently.



\*\*Request\*\*

```json

{

&nbsp; "encrypted\_seed": "BASE64\_STRING"

}

````



\*\*Response\*\*



```json

{

&nbsp; "status": "ok"

}

````



---



\## GET `/generate-2fa`



Generates the current TOTP code using the stored seed.



\*\*Response\*\*

```json

{

&nbsp; "code": "123456",

&nbsp; "valid\_for": 30

}

````



---



\## POST `/verify-2fa`



Verifies a provided TOTP code with ±1 time-window tolerance.



\*\*Request\*\*

```json

{

&nbsp; "code": "123456"

}

````

\*\*Response\*\*

```json

{

&nbsp; "valid": true

}

````



---



\## Persistent Storage



\- The decrypted seed is stored at `/data/seed.txt`

\- Docker volumes ensure the seed persists across container restarts

\- Cron output is stored at `/cron/last\_code.txt`



---



\## Cron Job Output



The cron job runs every minute and logs the generated TOTP code to:



```

/cron/last\_code.txt

```

\*\*Example\*\*

```

2025-12-13 18:18:01 - 2FA Code: 508931

```



---



\## Project Structure

```pki-2faa/

│

├── app/

│   └── main.py

│

├── scripts/

│   └── log\_2fa\_cron.py

│

├── cron/

│   └── 2fa-cron

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── student\_private.pem

├── student\_public.pem

├── instructor\_public.pem

├── request\_seed.py

├── .gitignore

├── .gitattributes

└── README.md

```

---

\## Docker Setup



Build the Docker image and start the service using Docker Compose:



```bash

docker-compose build

docker-compose up -d

````



---



\## Commit Proof



The final Git commit hash is cryptographically signed using the student private RSA key

(RSA-PSS with SHA-256).



The signature is then encrypted using the instructor public RSA key

(RSA-OAEP with SHA-256) and Base64 encoded for submission verification.



The `sign\_commit.py` script automates this entire process.



---



\## Security Notes



\- Cryptographic keys are committed only for assignment and evaluation purposes.

\- RSA OAEP and TOTP implementations follow standard cryptographic best practices.

\- UTC timezone is enforced to prevent TOTP time-drift mismatches.

\- Docker volumes are used to isolate persistent data from the container lifecycle.





---





\## Conclusion



This microservice demonstrates secure authentication system design using cryptography,

containerization, persistent storage, background scheduling, and verifiable commit

integrity.



