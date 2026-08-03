def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 33:
        return "E"
    else:
        return "F"


def calculate_result(subjects: dict):
    """Returns (total, percentage, grade, status) for a subjects dict."""
    if not subjects:
        return 0, 0.0, "N/A", "N/A"

    total = sum(subjects.values())
    max_total = len(subjects) * 100
    percentage = round((total / max_total) * 100, 2) if max_total else 0.0

    grade = get_grade(percentage)
    status = "PASS" if all(m >= 33 for m in subjects.values()) else "FAIL"

    return total, percentage, grade, status


def get_ranking(db):
    """Returns list of (roll_no, name, percentage, grade, status) sorted desc by %."""
    results = []
    for roll_no, data in db.all_students().items():
        total, pct, grade, status = calculate_result(data["subjects"])
        results.append((roll_no, data["name"], pct, grade, status))
    results.sort(key=lambda x: x[2], reverse=True)
    return results