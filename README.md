# PKI-Based 2FA Authentication Microservice



## Overview

This project implements a secure, containerized authentication microservice using Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) based two-factor authentication. It demonstrates real-world security practices such as RSA cryptography, TOTP verification, Docker containerization, cron jobs, and persistent storage.



The service decrypts a secure seed using RSA, generates TOTP codes, verifies user-provided codes, and periodically logs TOTP values using a cron job.



---



## Features

- RSA 4096-bit key–based seed decryption (OAEP with SHA-256)
- TOTP-based 2FA (SHA-1, 30-second window, 6-digit codes)
- REST API with three endpoints
- Cron job running every minute to log TOTP codes
- Dockerized using a multi-stage build
- Persistent storage using Docker volumes
- UTC timezone enforced across API and cron jobs

---

## API Endpoints

### POST `/decrypt-seed`

Decrypts the encrypted seed using the student private key and stores it persistently.

**Request**
```json
{
 "encrypted_seed": "BASE64_STRING"
}
````

**Response**
```json
{
 "status": "ok"
}
````

---

## GET `/generate-2fa`
Generates the current TOTP code using the stored seed.
**Response**
```json
{
 "code": "123456",
 "valid_for": 30
}
````

---

## POST `/verify-2fa`
Verifies a provided TOTP code with ±1 time-window tolerance.

**Request**
```json
{
 "code": "123456"
}
````

**Response**
```json
{
 "valid": true
}
````

---

## Persistent Storage

- The decrypted seed is stored at `/data/seed.txt`
- Docker volumes ensure the seed persists across container restarts
- Cron output is stored at `/cron/last_code.txt`
  
---

## Cron Job Output
The cron job runs every minute and logs the generated TOTP code to:

```
/cron/last_code.txt
```

**Example**

```
2025-12-13 18:18:01 - 2FA Code: 508931
```

---

## Project Structure

```
pki-2faa/

│

├── app/

│   └── main.py

│

├── scripts/

│   └── log_2fa_cron.py

│

├── cron/

│   └── 2fa-cron

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── student_private.pem

├── student_public.pem

├── instructor_public.pem

├── request_seed.py

├── .gitignore

├── .gitattributes

└── README.md

```

---

## Docker Setup

Build the Docker image and start the service using Docker Compose:

```bash
docker-compose build
docker-compose up -d
````

---

## Security Notes

- Cryptographic keys are committed only for assignment and evaluation purposes.
- RSA OAEP and TOTP implementations follow standard cryptographic best practices.
- UTC timezone is enforced to prevent TOTP time-drift mismatches.
- Docker volumes are used to isolate persistent data from the container lifecycle.

---

## Conclusion

This microservice demonstrates secure authentication system design using cryptography,
containerization, persistent storage, background scheduling, and verifiable commit
integrity.



