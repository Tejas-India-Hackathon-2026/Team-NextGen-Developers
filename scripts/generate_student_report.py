import json
import os
import sys

def generate_report(username: str, users_path: str = "users.json", attendance_path: str = "attendance.json"):
    """Generate a formatted terminal summary report for a student."""
    if not os.path.exists(users_path):
        print(f"[ERROR] Users file '{users_path}' missing.")
        return
        
    with open(users_path, "r", encoding="utf-8") as f:
        users = json.load(f)
        
    user = users.get(username)
    if not user:
        print(f"[ERROR] User '{username}' not found.")
        return
        
    attendance_data = []
    if os.path.exists(attendance_path):
        with open(attendance_path, "r", encoding="utf-8") as f:
            raw = json.load(f).get(username, [])
            attendance_data = raw if isinstance(raw, list) else []
            
    print("=" * 55)
    print(f" STUDENT ACADEMIC PROFILE: {user.get('name', username).upper()}")
    print("=" * 55)
    print(f" Username : {username}")
    print(f" Role     : {user.get('role', 'student').capitalize()}")
    print(f" Karma    : {user.get('karma', 0)} pts")
    print(f" Badges   : {', '.join(user.get('badges', [])) or 'None'}")
    print("-" * 55)
    print(" ATTENDANCE SUMMARY:")
    if attendance_data:
        for stats in attendance_data:
            subj = stats.get("subject", "Unknown")
            attended = stats.get("attended", 0)
            total = stats.get("total", 0)
            pct = round((attended / total * 100), 1) if total > 0 else 0
            status_flag = "[SAFE]" if pct >= 75 else "[SHORTAGE]"
            print(f"  - {subj:<35}: {attended}/{total} ({pct}%) {status_flag}")
    else:
        print("  No attendance records logged.")
    print("=" * 55)

if __name__ == "__main__":
    target_user = sys.argv[1] if len(sys.argv) > 1 else "sarika123"
    generate_report(target_user)
