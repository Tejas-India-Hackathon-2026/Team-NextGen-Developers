from datetime import datetime, date

def calculate_days_remaining(exam_date_str: str) -> int:
    """Calculate days left until the exam date (YYYY-MM-DD)."""
    try:
        exam_dt = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        today = date.today()
        diff = (exam_dt - today).days
        return max(0, diff)
    except Exception:
        return 0

def generate_revision_plan(subject: str, units: list, exam_date_str: str, study_hours_per_day: float = 3.0) -> dict:
    """Generate a phased daily revision roadmap for an upcoming semester exam."""
    days_left = calculate_days_remaining(exam_date_str)
    total_units = len(units)
    
    if total_units == 0:
        return {"subject": subject, "days_left": days_left, "status": "No units provided", "schedule": []}
        
    days_per_unit = max(1, days_left // total_units) if days_left > 0 else 1
    
    schedule = []
    current_day = 1
    for unit in units:
        schedule.append({
            "unit": unit,
            "target_days": f"Day {current_day} to Day {min(days_left, current_day + days_per_unit - 1)}",
            "allocated_hours": round(days_per_unit * study_hours_per_day, 1),
            "milestone": f"Complete theory, solved examples, and previous year questions for {unit}"
        })
        current_day += days_per_unit
        
    return {
        "subject": subject,
        "exam_date": exam_date_str,
        "days_left": days_left,
        "total_units": total_units,
        "urgency": "HIGH" if days_left <= 7 else "MEDIUM" if days_left <= 21 else "LOW",
        "schedule": schedule
    }
