def calculate_attendance_percentage(attended: int, total: int) -> float:
    if total <= 0: return 0.0
    return round((attended / total) * 100.0, 1)

def simulate_future_attendance(curr_att: int, curr_tot: int, bunks: int, future_att: int) -> dict:
    tot = curr_tot + bunks + future_att
    att = curr_att + future_att
    pct = calculate_attendance_percentage(att, tot)
    return {'projected_pct': pct, 'is_safe_75': pct >= 75.0}
