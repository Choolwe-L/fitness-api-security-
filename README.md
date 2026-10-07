# Fitness API — Security Assessment & Hardening Framework

> JPR Solutions · 12-Week Internship Project · Cybersecurity (Fitness & Wellness)

A 12-week project to perform a full API penetration test of a deliberately
vulnerable **Fitness API**, write custom Python security tooling, and deliver a
**hardened, securely configured Flask API** with basic cloud infrastructure.

**Project goal:** a fully documented API penetration test report, a collection of
custom Python security scripts, and a hardened Flask API deployed with basic
cloud infrastructure — demonstrating a comprehensive understanding of the API
security lifecycle.

---

## Week 1 — Foundations of Web & API Security ✅

**Objective:** understand core web/API communication and attack vectors, and
stand up a secure development and testing environment.

### Deliverables status
- [x] Project GitHub repository created with a README
- [x] Security testing environment configured (Kali Linux + Docker)
- [x] Basic Flask API running locally
- [ ] Repository link submitted on the JPR portal (Tasks page) — *manual step*

### Environment
| Tool | Version |
|------|---------|
| OS | Kali Linux (security tooling distro) |
| Python | 3.14 |
| Flask | 3.1.3 |
| Git | 2.53 |
| Docker | 28.5 |

See [`docs/environment-setup.md`](docs/environment-setup.md) for details and
[`docs/week1-foundations.md`](docs/week1-foundations.md) for the HTTP/HTTPS, API
authentication, and OWASP notes.

---

## The target API

[`app/app.py`](app/app.py) is a **deliberately vulnerable** Flask fitness API.
It is the target for the assessment in later weeks and contains intentional
instances of the OWASP API Security Top 10 (IDOR, broken auth, excessive data
exposure, SQL injection, no rate limiting, debug mode, hardcoded secret).

> ⚠️ **Run locally only.** Do not expose this service to the public internet.

### Run it locally

```bash
# 1. (optional) create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. run the API (seeds a local SQLite DB on first run)
python app/app.py
# -> http://127.0.0.1:5000
```

### Run with Docker

```bash
docker compose up --build
# -> http://127.0.0.1:5000
```

### Smoke test

```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/api/workouts
curl -X POST http://127.0.0.1:5000/api/login \
     -H 'Content-Type: application/json' \
     -d '{"username":"alice","password":"password123"}'
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET  | `/` | Service info / endpoint list |
| POST | `/api/register` | Create a user (`username`, `password`, `email`) |
| POST | `/api/login` | Log in, returns a token |
| GET  | `/api/users/<id>` | Fetch a user by id |
| GET  | `/api/workouts?user_id=<id>` | List workouts |
| POST | `/api/workouts` | Create a workout |
| GET  | `/api/search?activity=<name>` | Search workouts by activity |

---

## Repository layout

```
fitness-api-security/
├── app/            # the vulnerable Flask API (the assessment target)
├── docs/           # weekly notes, findings, and the pentest report
├── scripts/        # custom Python security scripts (added in later weeks)
├── tests/          # tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 12-week roadmap
1. **Foundations of Web & API Security** *(current)*
2. Reconnaissance & API enumeration
3. Authentication & authorization testing
4. Injection & input-validation attacks
5. Business-logic & rate-limiting flaws
6. Custom Python security scripting
7. Automated scanning & reporting
8. Hardening: authentication & authorization
9. Hardening: input validation & secrets management
10. Secure deployment & cloud infrastructure
11. Final penetration test & documentation
12. Final report & presentation
