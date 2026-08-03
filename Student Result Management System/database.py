import json
import os
from datetime import datetime

DATA_FILE = "students_data.json"


class StudentDatabase:
    def __init__(self, filename=DATA_FILE):
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