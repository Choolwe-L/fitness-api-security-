# Week 1 — Foundations of Web & API Security (Notes)

Study notes covering the Week 1 learning objectives: HTTP/HTTPS, request/response
structure, API authentication types, and the OWASP Top 10.

---

## 1. HTTP vs HTTPS

- **HTTP** (HyperText Transfer Protocol): stateless, text-based request/response
  protocol between a client and a server. Default port **80**. Data travels in
  **plaintext** — anyone on the path can read it.
- **HTTPS**: HTTP over **TLS**. Default port **443**. Encrypts the traffic and
  authenticates the server via certificates, protecting against eavesdropping and
  tampering (man-in-the-middle). APIs handling credentials or personal data
  **must** use HTTPS.

## 2. Request / response structure

**Request**
```
POST /api/login HTTP/1.1          <- method, path, version (request line)
Host: api.example.com             <- headers
Content-Type: application/json
Authorization: Bearer <token>

{"username":"alice","password":"..."}   <- body
```

**Response**
```
HTTP/1.1 200 OK                   <- version, status code, reason (status line)
Content-Type: application/json    <- headers
Content-Length: 42

{"token":"...","user_id":1}       <- body
```

### Common methods
| Method | Purpose | Safe | Idempotent |
|--------|---------|------|-----------|
| GET | read a resource | yes | yes |
| POST | create / submit | no | no |
| PUT | replace a resource | no | yes |
| PATCH | partial update | no | no |
| DELETE | remove a resource | no | yes |

### Status code families
| Range | Meaning |
|-------|---------|
| 1xx | Informational |
| 2xx | Success (200 OK, 201 Created, 204 No Content) |
| 3xx | Redirection (301, 302, 304) |
| 4xx | Client error (400, 401, 403, 404, 429) |
| 5xx | Server error (500, 502, 503) |

## 3. API authentication types

| Type | How it works | Notes / risks |
|------|--------------|---------------|
| **Basic auth** | `Authorization: Basic base64(user:pass)` | base64 is *not* encryption — only safe over HTTPS |
| **API keys** | shared secret in a header/query param | no per-user identity; leaks easily if in URLs |
| **Bearer / JWT** | signed token in `Authorization: Bearer <jwt>` | stateless; must validate signature, expiry, and claims |
| **OAuth 2.0** | delegated authorization via access tokens | standard for third-party access; complex to implement correctly |
| **Session cookies** | server-side session id stored in a cookie | needs `HttpOnly`, `Secure`, `SameSite` flags + CSRF protection |

**AuthN vs AuthZ**
- **Authentication** = *who are you?* (verifying identity)
- **Authorization** = *what are you allowed to do?* (verifying permissions)

## 4. OWASP API Security Top 10 (2023) — quick reference

| ID | Risk |
|----|------|
| API1 | Broken Object Level Authorization (BOLA / IDOR) |
| API2 | Broken Authentication |
| API3 | Broken Object Property Level Authorization (excessive data exposure) |
| API4 | Unrestricted Resource Consumption (no rate limiting) |
| API5 | Broken Function Level Authorization |
| API6 | Unrestricted Access to Sensitive Business Flows |
| API7 | Server Side Request Forgery (SSRF) |
| API8 | Security Misconfiguration |
| API9 | Improper Inventory Management |
| API10 | Unsafe Consumption of APIs |

## 5. Vulnerabilities planted in our target API

The target (`app/app.py`) contains these intentional flaws to be assessed and
fixed in later weeks:

| Finding | OWASP mapping | Where |
|---------|---------------|-------|
| IDOR — any user's workouts readable | API1 | `GET /api/workouts?user_id=` |
| IDOR — any user record readable | API1 | `GET /api/users/<id>` |
| Plaintext passwords; predictable non-expiring token | API2 | `register` / `login` |
| Password returned in user response | API3 | `GET /api/users/<id>` |
| No rate limiting on login | API4 | `POST /api/login` |
| SQL injection | Injection | `login`, `search` |
| Debug mode on, hardcoded secret, bound to 0.0.0.0 | API8 | app config / `app.run` |

## References
- Mozilla HTTP Overview — https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- OWASP API Security Top 10 — https://owasp.org/API-Security/editions/2023/en/0x00-introduction/
- Flask Quickstart — https://flask.palletsprojects.com/en/latest/quickstart/
