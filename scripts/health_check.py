import json
import os
import sys

def check_file(path: str, is_json: bool = True) -> tuple:
    """Verify file existence, readability, and JSON validity."""
    if not os.path.exists(path):
        return False, "File does not exist"
    if is_json:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return True, f"Valid JSON ({type(data).__name__}, len={len(data)})"
        except Exception as e:
            return False, f"Corrupted JSON: {e}"
    return True, f"File exists ({os.path.getsize(path)} bytes)"

def run_diagnostics():
    print("=" * 60)
    print("[DIAGNOSTIC] Student Resource Platform - System Diagnostics")
    print("=" * 60)
    
    files_to_check = [
        ("users.json", True),
        ("materials_meta.json", True),
        ("announcements.json", True),
        ("attendance.json", True),
        ("timetable.json", True),
        ("data/departments.json", True),
        ("data/faqs.json", True),
        ("data/internships.json", True),
        ("data/quiz_questions.json", True),
        ("data/flashcards.json", True),
        ("data/faculty_directory.json", True),
        ("materials/", False)
    ]
    
    all_ok = True
    for path, is_json in files_to_check:
        if path.endswith("/"):
            exists = os.path.exists(path) and os.path.isdir(path)
            status = "Directory OK" if exists else "Missing directory"
            ok = exists
        else:
            ok, status = check_file(path, is_json)
            
        badge = "[OK]  " if ok else "[FAIL]"
        print(f"{badge} {path:<30} -> {status}")
        if not ok:
            all_ok = False
            
    print("-" * 60)
    if all_ok:
        print("[SUCCESS] All core datasets and directories are healthy!")
        sys.exit(0)
    else:
        print("[WARNING] System diagnostic warnings found.")
        sys.exit(1)

if __name__ == "__main__":
    run_diagnostics()
