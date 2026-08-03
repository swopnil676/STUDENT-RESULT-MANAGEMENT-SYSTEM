from database import StudentDatabase
from ui_helpers import clear_screen, pause
from actions import (
    action_add_student,
    action_view_all,
    action_search,
    action_update,
    action_delete,
    action_report_card,
    action_ranking,
)

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