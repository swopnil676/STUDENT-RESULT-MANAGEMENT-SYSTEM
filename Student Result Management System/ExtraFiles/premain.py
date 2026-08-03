import json
import os
from datetime import datetime

DATA_FILE = "students_data.json"


# --------------------------------------------------------------------------
# Data Layer
# --------------------------------------------------------------------------
class StudentDatabase:
    def _init_(self, filename=DATA_FILE):
        self.filename = filename
        self.students = {}  # key: roll_no (str) -> dict
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.students = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.students = {}
        else:
            self.students = {}

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, roll_no, name, subjects):
        self.students[roll_no] = {
            "name": name,
            "subjects": subjects,  # dict: subject -> marks
            "created_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.save()

    def delete_student(self, roll_no):
        if roll_no in self.students:
            del self.students[roll_no]
            self.save()
            return True
        return False

    def update_marks(self, roll_no, subjects):
        if roll_no in self.students:
            self.students[roll_no]["subjects"] = subjects
            self.save()
            return True
        return False

    def update_name(self, roll_no, name):
        if roll_no in self.students:
            self.students[roll_no]["name"] = name
            self.save()
            return True
        return False

    def get_student(self, roll_no):
        return self.students.get(roll_no)

    def search_by_name(self, name):
        name = name.lower()
        return {
            r: s for r, s in self.students.items()
            if name in s["name"].lower()
        }

    def all_students(self):
        return self.students


# --------------------------------------------------------------------------
# Business Logic
# --------------------------------------------------------------------------
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


def get_ranking(db: StudentDatabase):
    """Returns list of (roll_no, name, percentage, grade, status) sorted desc by %."""
    results = []
    for roll_no, data in db.all_students().items():
        total, pct, grade, status = calculate_result(data["subjects"])
        results.append((roll_no, data["name"], pct, grade, status))
    results.sort(key=lambda x: x[2], reverse=True)
    return results


# --------------------------------------------------------------------------
# Console Helpers
# --------------------------------------------------------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def get_valid_marks_input():
    """Prompt for subjects until user is done; validate 0-100 range."""
    subjects = {}
    print("Enter subject name and marks (0-100). Type 'done' as subject name to finish.")
    while True:
        subject = input("  Subject name: ").strip()
        if subject.lower() == "done":
            if not subjects:
                print("  You must add at least one subject.")
                continue
            break
        if not subject:
            print("  Subject name cannot be empty.")
            continue
        marks_raw = input(f"  Marks for {subject}: ").strip()
        try:
            marks = float(marks_raw)
            if not (0 <= marks <= 100):
                print("  Marks must be between 0 and 100.")
                continue
        except ValueError:
            print("  Invalid number, try again.")
            continue
        subjects[subject] = marks
    return subjects


# --------------------------------------------------------------------------
# Menu Actions
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# Main Menu Loop
# --------------------------------------------------------------------------
MENU = """
  STUDENT RESULT MANAGEMENT SYSTEM
------------------------------------
  1. Add Student
  2. View All Students
  3. Search Student
  4. Update Student
  5. Delete Student
  6. Generate Report Card
  7. View Class Ranking
  8. Exit
------------------------------------
"""


def main():
    db = StudentDatabase()

    while True:
        clear_screen()
        print(MENU)
        choice = input("Enter your choice (1-8): ").strip()

        clear_screen()
        if choice == "1":
            action_add_student(db)
        elif choice == "2":
            action_view_all(db)
        elif choice == "3":
            action_search(db)
        elif choice == "4":
            action_update(db)
        elif choice == "5":
            action_delete(db)
        elif choice == "6":
            action_report_card(db)
        elif choice == "7":
            action_ranking(db)
        elif choice == "8":
            print("Thank you for using the Student Result Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 8.")

        pause()


if __name__ == "__main__":
    main()