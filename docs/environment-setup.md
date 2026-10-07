# Environment Setup — Week 1

## Security testing environment

This project uses **Kali Linux** as the security tooling environment. Kali is a
Debian-based distribution that ships with the penetration-testing tools used in
later weeks (curl, nmap, sqlmap, Burp Suite, etc.), satisfying the Week 1
requirement for a "configured security testing environment (VM/Docker)."

A **Docker** environment is also provided so the target API can be run in an
isolated, reproducible container (see the `Dockerfile` and `docker-compose.yml`
at the repo root).

## Installed tooling

| Requirement | Tool | Version | Status |
|-------------|------|---------|--------|
| Linux VM / environment | Kali Linux | rolling | ✅ |
| Containerization | Docker | 28.5 | ✅ |
| Language runtime | Python | 3.14 | ✅ |
| Web framework | Flask | 3.1.3 | ✅ |
| Version control | Git | 2.53 | ✅ |
| Web browser | Firefox (Kali default) | — | ✅ |
| Editor | VS Code | optional | install via `sudo apt install code` or use any editor |

## Verify your environment

```bash
python3 --version
pip3 --version
git --version
docker --version
python3 -c "import flask; print('Flask OK')"
```

## Python virtual environment (recommended)

```bash
cd fitness-api-security
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Git configuration

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```
