import json
import os
import sys

def audit_security(root_dir: str = "."):
    """Audit project for common security risks, sensitive file exposure, and weak password defaults."""
    print("=" * 60)
    print("[SECURITY AUDIT] Student Resource Platform Security Scan")
    print("=" * 60)
    
    warnings = []
    
    # 1. Check for uncommitted .env or credentials
    suspicious_patterns = [".env", ".key", "id_rsa", "credentials.json", "secret.txt"]
    for root, _, files in os.walk(root_dir):
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            for pat in suspicious_patterns:
                if pat in file.lower() and not file.endswith(".example"):
                    warnings.append(f"Sensitive file found: {os.path.join(root, file)}")
                    
    # 2. Check users.json for plain-text password hashes
    users_path = os.path.join(root_dir, "users.json")
    if os.path.exists(users_path):
        try:
            with open(users_path, "r", encoding="utf-8") as f:
                users = json.load(f)
            for uname, udata in users.items():
                pwd = udata.get("password", "")
                if len(pwd) != 64:  # SHA256 hex length
                    warnings.append(f"User '{uname}' password hash does not appear to be SHA-256 (length: {len(pwd)})")
        except Exception as e:
            warnings.append(f"Failed to read users.json: {e}")
            
    # 3. Check materials directory for executable files
    materials_dir = os.path.join(root_dir, "materials")
    if os.path.exists(materials_dir):
        for f in os.listdir(materials_dir):
            ext = os.path.splitext(f)[1].lower()
            if ext in [".exe", ".bat", ".sh", ".cmd", ".js", ".vbs"]:
                warnings.append(f"Executable file in materials directory: {f}")
                
    if warnings:
        print(f"[WARN] Security findings detected ({len(warnings)} issues):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("[PASS] No immediate security vulnerabilities or exposed secrets found.")
        
    print("=" * 60)

if __name__ == "__main__":
    audit_security()
