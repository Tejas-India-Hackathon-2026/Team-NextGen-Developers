from modules.attendance_forecast import calculate_attendance_percentage, simulate_future_attendance

def test_calc():
    assert calculate_attendance_percentage(15, 20) == 75.0

def test_simulation():
    sim = simulate_future_attendance(15, 20, bunks=2, future_att=2)
    assert sim['projected_pct'] == round(17/24*100, 1)
