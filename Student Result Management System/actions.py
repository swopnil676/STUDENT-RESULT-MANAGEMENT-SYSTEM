from logic import calculate_result, get_ranking
from ui_helpers import print_header, get_valid_marks_input


def action_add_student(db):
    print_header("ADD NEW STUDENT")

    roll_no = input("Roll Number: ").strip()
    if not roll_no:
        print("Roll number cannot be empty.")
        return
    if db.get_student(roll_no):
        print("A student with this roll number already exists.")
        return
    
    name = input("Student Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    
    subjects = get_valid_marks_input()
    db.add_student(roll_no, name, subjects)
    print(f"\nStudent '{name}' (Roll No: {roll_no}) added successfully!")


def action_view_all(db):
    print_header("ALL STUDENTS")
    students = db.all_students()
    if not students:
        print("No student records found.")
        return
    print(f"{'Roll No':<10}{'Name':<20}{'Total':<10}{'%':<10}{'Grade':<8}{'Status':<8}")
    print("-" * 66)
    for roll_no, data in students.items():
        total, pct, grade, status = calculate_result(data["subjects"])
        print(f"{roll_no:<10}{data['name']:<20}{total:<10}{pct:<10}{grade:<8}{status:<8}")


def action_search(db):
    print_header("SEARCH STUDENT")
    print("1. Search by Roll Number")
    print("2. Search by Name")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        roll_no = input("Enter Roll Number: ").strip()
        student = db.get_student(roll_no)
        if student:
            show_student_detail(roll_no, student)
        else:
            print("No student found with that roll number.")
    elif choice == "2":
        name = input("Enter Name (or part of it): ").strip()
        matches = db.search_by_name(name)
        if matches:
            for roll_no, data in matches.items():
                show_student_detail(roll_no, data)
        else:
            print("No matching students found.")
    else:
        print("Invalid choice.")


def show_student_detail(roll_no, data):
    total, pct, grade, status = calculate_result(data["subjects"])
    print("\n" + "-" * 40)
    print(f"Roll No : {roll_no}")
    print(f"Name    : {data['name']}")
    print("Subjects:")
    for sub, marks in data["subjects"].items():
        print(f"   - {sub}: {marks}")
    print(f"Total   : {total}")
    print(f"Percent : {pct}%")
    print(f"Grade   : {grade}")
    print(f"Status  : {status}")
    print("-" * 40)


def action_update(db):
    print_header("UPDATE STUDENT")
    roll_no = input("Enter Roll Number to update: ").strip()
    student = db.get_student(roll_no)
    if not student:
        print("No student found with that roll number.")
        return

    print(f"Current Name: {student['name']}")
    print("1. Update Name")
    print("2. Update Marks")
    print("3. Update Both")
    choice = input("Choose an option: ").strip()

    if choice in ("1", "3"):
        new_name = input("New Name: ").strip()
        if new_name:
            db.update_name(roll_no, new_name)
    if choice in ("2", "3"):
        new_subjects = get_valid_marks_input()
        db.update_marks(roll_no, new_subjects)

    print("Student record updated successfully!")


def action_delete(db):
    print_header("DELETE STUDENT")
    roll_no = input("Enter Roll Number to delete: ").strip()
    student = db.get_student(roll_no)
    if not student:
        print("No student found with that roll number.")
        return
    confirm = input(f"Are you sure you want to delete '{student['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        db.delete_student(roll_no)
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def action_report_card(db):
    print_header("STUDENT REPORT CARD")
    roll_no = input("Enter Roll Number: ").strip()
    student = db.get_student(roll_no)
    if not student:
        print("No student found with that roll number.")
        return

    ranking = get_ranking(db)
    rank = next((i + 1 for i, r in enumerate(ranking) if r[0] == roll_no), None)

    total, pct, grade, status = calculate_result(student["subjects"])

    print("\n" + "=" * 40)
    print("REPORT CARD".center(40))
    print("=" * 40)
    print(f"Roll No     : {roll_no}")
    print(f"Name        : {student['name']}")
    print("-" * 40)
    print(f"{'Subject':<20}{'Marks':<10}")
    for sub, marks in student["subjects"].items():
        print(f"{sub:<20}{marks:<10}")
    print("-" * 40)
    print(f"Total Marks : {total} / {len(student['subjects']) * 100}")
    print(f"Percentage  : {pct}%")
    print(f"Grade       : {grade}")
    print(f"Result      : {status}")
    print(f"Class Rank  : {rank} of {len(ranking)}")
    print("=" * 40)


def action_ranking(db):
    print_header("CLASS RANKING (by percentage)")
    ranking = get_ranking(db)
    if not ranking:
        print("No student records found.")
        return
    print(f"{'Rank':<6}{'Roll No':<10}{'Name':<20}{'%':<10}{'Grade':<8}{'Status':<8}")
    print("-" * 62)
    for i, (roll_no, name, pct, grade, status) in enumerate(ranking, start=1):
        print(f"{i:<6}{roll_no:<10}{name:<20}{pct:<10}{grade:<8}{status:<8}")