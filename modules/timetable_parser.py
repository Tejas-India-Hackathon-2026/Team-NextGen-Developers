def find_schedule_conflicts(schedule_list: list) -> list:
    """Detect time collisions in a student's daily or weekly class schedule."""
    conflicts = []
    # schedule format: [{"day": "Monday", "start": "09:00", "end": "10:00", "subject": "DSA"}, ...]
    days = {}
    for slot in schedule_list:
        day = slot.get("day", "Monday")
        if day not in days:
            days[day] = []
        days[day].append(slot)
        
    for day, slots in days.items():
        for i in range(len(slots)):
            for j in range(i + 1, len(slots)):
                s1, s2 = slots[i], slots[j]
                # Compare time intervals
                if not (s1.get("end") <= s2.get("start") or s2.get("end") <= s1.get("start")):
                    conflicts.append({
                        "day": day,
                        "slot1": s1,
                        "slot2": s2,
                        "reason": f"Overlap between {s1.get('subject')} and {s2.get('subject')}"
                    })
    return conflicts

def find_common_free_slots(user_schedules: dict, day: str, all_slots: list = None) -> list:
    """Find mutual free study group slots across multiple students."""
    if all_slots is None:
        all_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "14:00-15:00", "15:00-16:00", "16:00-17:00"]
        
    free_slots = set(all_slots)
    for username, sched in user_schedules.items():
        busy_for_day = set()
        for slot in sched:
            if slot.get("day") == day:
                time_range = f"{slot.get('start')}-{slot.get('end')}"
                busy_for_day.add(time_range)
        free_slots -= busy_for_day
        
    return sorted(list(free_slots))
