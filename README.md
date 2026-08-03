# 📚 Student Result Management System

A **Python-based Student Result Management System** designed to manage student records, calculate academic results, generate report cards, and display class rankings. The project follows a **modular architecture** with separate layers for data management, business logic, and user interface, making it clean, maintainable, and easy to extend.

---

# 📌 Overview

This project simplifies the process of managing student academic records through a menu-driven command-line interface. It supports complete CRUD operations, automatic result calculation, report card generation, and class ranking while storing data persistently using JSON.

---

# ✨ Features

* 👨‍🎓 Add new student records
* 📋 View all students
* 🔍 Search students by roll number or name
* ✏️ Update student details and marks
* 🗑️ Delete student records
* 📝 Generate individual report cards
* 🏆 Display class rankings
* 📊 Automatic percentage and grade calculation
* 💾 JSON-based persistent data storage
* ⚠️ Input validation and error handling

---

# 🛠️ Technologies Used

* **Python**
* **Object-Oriented Programming (OOP)**
* **JSON File Handling**
* **Command-Line Interface (CLI)**
* **Modular Programming**

---

# 📁 Project Structure

```text
Student-Result-Management-System/
│
├── database.py          # Student database (CRUD + JSON storage)
├── logic.py             # Result calculation and ranking logic
├── ui_helpers.py        # Console UI helper functions
├── actions.py           # Menu action handlers
├── main.py              # Application entry point
├── students_data.json   # Student data storage
└── README.md
```

---

# 📖 Workflow

```text
Program Start
      │
      ▼
main.py
      │
      ▼
Create StudentDatabase
      │
      ▼
Load students_data.json
      │
      ▼
Display Main Menu
      │
      ▼
User Selects Option
      │
      ▼
Execute Action
(Add / View / Search / Update /
Delete / Report Card / Ranking)
      │
      ▼
Save Changes (if required)
      │
      ▼
Return to Main Menu
      │
      ▼
Exit Program
```

---

# 🚀 How to Run

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Open the Project

```bash
cd Student-Result-Management-System
```

### 3. Run the Application

```bash
python3 main.py
```

---

# 🔄 Data Flow

```text
students_data.json
        ▲
        │
        ▼
StudentDatabase (database.py)
        │
        ▼
actions.py
        │
        ▼
logic.py
        │
        ▼
ui_helpers.py
```

---

# 📂 Module Responsibilities

### 📄 database.py

* Manages student records
* Performs CRUD operations
* Loads and saves `students_data.json`
* Independent data layer

### 📄 logic.py

* Calculates percentage
* Determines grades
* Generates class rankings
* Contains business logic only

### 📄 ui_helpers.py

* Handles console formatting
* Clears screen
* Displays headers
* Validates marks input

### 📄 actions.py

* Handles all menu operations
* Connects UI, database, and business logic
* Executes user-selected actions

### 📄 main.py

* Entry point of the application
* Displays menu
* Dispatches actions
* Controls the main application loop

### 📄 students_data.json

* Stores student records persistently
* Loaded automatically when the application starts

---

# 🔮 Future Improvements

* 🖥️ Graphical User Interface (Tkinter/PyQt)
* 🗄️ MySQL or SQLite database integration
* 📤 Export report cards as PDF
* 🔐 User authentication
* 📈 Student performance analytics
* 🌐 Web-based version using Flask or Django

---

# 👨‍💻 Author

**Swopnil Biswas**

B.Tech – Electronics & Communication Engineering

---

⭐ **A practical Python project built to strengthen Object-Oriented Programming, JSON file handling, modular programming, and problem-solving skills through real-world application development.**

