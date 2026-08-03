import os


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