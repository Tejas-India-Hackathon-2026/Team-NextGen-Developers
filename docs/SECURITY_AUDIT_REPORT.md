# 🛡️ Security Audit & Mitigation Report

This security report details the threat model, vulnerability assessments, and defensive layers implemented in the **Student Resource Sharing Platform**.

---

## 1. Threat Model & Vector Analysis

| Threat | Risk Level | Implemented Mitigation |
|---|---|---|
| **Malicious PDF Payloads** | High | `PyPDF` content scanning, page inspection, and script execution prevention |
| **Directory Traversal in Uploads** | High | Filename sanitization with basename isolation in `modules/sanitizer.py` |
| **Brute Force Authentication** | Medium | Rate limiter sliding window mechanism in `modules/rate_limiter.py` |
| **Cross-Site Scripting (XSS)** | Medium | HTML tag stripping and entity escaping in `modules/sanitizer.py` |
| **Credential Compromise** | High | SHA-256 password hashing; no plain-text passwords stored |
| **Duplicate/Spam Submissions** | Low | Cosine similarity plagiarism checker in `modules/plagiarism_checker.py` |

---

## 2. Automated Security Workflows
- Continuous static analysis via `.github/workflows/security.yml`
- Dependabot automated vulnerability monitoring via `.github/dependabot.yml`
- Local pre-commit security scanner via `python scripts/security_audit.py`
