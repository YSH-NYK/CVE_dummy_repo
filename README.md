# Sentinel Demo Microservice App (CVE Fixer Test Target)

A multi-ecosystem demo repository representing a cloud microservice stack combining Python (Flask / APIs), Node.js (Gateway & utilities), and multi-stage container definitions (`Dockerfile`).

This repository serves as a target test object for the Sentinel CVE Fixer pipeline (Locator Agent, Fixer Agent, and Verifier Agent).

---

## Architecture & Components

```
├── Dockerfile                  # Primary Alpine container image (vulnerable openssl OS package)
├── docker/
│   └── Dockerfile.debian       # Debian-based secondary image definition
├── requirements.txt            # Core Python backend dependencies (PyYAML, urllib3, Jinja2, Pillow, Flask)
├── requirements-dev.txt        # Development dependencies (duplicate urllib3 declaration)
├── requirements-test.txt       # Test runner dependencies (duplicate PyYAML declaration)
├── package.json                # Node.js gateway dependencies (lodash, axios, underscore)
├── package-lock.json           # Node.js lockfile
├── src/
│   ├── app.py                  # Python Flask API service
│   └── index.js                # Node.js gateway utility
└── .gitignore
```

---

## Vulnerability & CVE Test Matrix

This repository includes real-world vulnerable package versions across multiple ecosystems to verify the CVE Fixer pipeline:

| Ecosystem | Package | Installed Version | Target CVE | Fixed In | Locations in Repo / Container |
|---|---|---|---|---|---|
| **Python** | `PyYAML` | `5.3` | `CVE-2020-14343` | `5.4` | `requirements.txt` (line 2), `requirements-test.txt` (line 4) |
| **Python** | `urllib3` | `1.26.4` | `CVE-2021-33503` | `1.26.5` | `requirements.txt` (line 3), `requirements-dev.txt` (line 3) |
| **Python** | `Jinja2` | `2.11.2` | `CVE-2021-44227` | `2.11.3` | `requirements.txt` (line 4) |
| **Python** | `Pillow` | `9.0.0` | `CVE-2022-24303` | `9.0.1` | `requirements.txt` (line 5) |
| **Node.js** | `lodash` | `4.17.15` | `CVE-2021-23337` | `4.17.21` | `package.json`, `package-lock.json` |
| **Node.js** | `axios` | `0.21.1` | `CVE-2021-3749` | `0.21.2` | `package.json`, `package-lock.json` |
| **Node.js** | `underscore` | `1.12.0` | `CVE-2021-23358` | `1.12.1` | `package.json`, `package-lock.json` |
| **OS / Image** | `openssl` / `libssl1.1` | `1.1.1k-r0` | `CVE-2021-3711` | `1.1.1l-r0` | Container image `alpine:3.14.0`, Dockerfile `FROM` line & `apk add` |

---

## Scenarios Handled

1. **Python CVE Location (Single & Multi-File)**: Identifies `PyYAML` and `urllib3` across manifest files.
2. **Node.js CVE Location**: Scans `package.json` and parses `package-lock.json` dependencies.
3. **Container Base Image Attribution (Rule R9)**: Maps OS vulnerabilities to `Dockerfile` `FROM alpine:3.14.0` line and package install commands.
4. **Read File from Repo**: Allows read-only inspection of source context (`src/app.py`, `src/index.js`, `requirements.txt`).
5. **Version Mismatch**: Verifies locator reports differences between declared version and scanned version.
6. **Missing Packages & Unknown CVEs**: Returns `not_found` and `lookup_failed` gracefully without pipeline failure.
