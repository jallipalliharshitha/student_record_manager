# Student Record Manager (Module 2 Assignment)

A complete Python application designed for managing student records. It incorporates input validation using **regular expressions (regex)**, robust **exception handling**, and data persistence directly readable and editable in **Windows Notepad**.

---

## Features & Assignment Requirements

| Requirement | Implementation in Project |
| :--- | :--- |
| **Add Student** | Prompts for Student ID, Name, Age, Course, and Email with strict validation on each field. |
| **Validate Email using Regex** | Uses the `re` module with pattern `^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$` to enforce valid email formats. |
| **Save Data to File** | Formatted text storage in `students.txt` that can be viewed and edited in **Notepad**. Includes a menu shortcut to launch Notepad directly. |
| **Read Student Data** | Reads `students.txt`, parses the pipe-separated fields back into `Student` objects, and displays them in a neat table. |
| **Handle Invalid Input using Exceptions** | Uses built-in exceptions (`ValueError`, `FileNotFoundError`) and custom exceptions (`InvalidEmailError`, `InvalidAgeError`, `DuplicateStudentError`, `StudentNotFoundError`) in dedicated `try...except` loops. |

---

## File Structure

```
student_record_manager/
├── student_manager.py             # Main application and interactive CLI
├── test_student_manager.py        # Unit test suite covering regex, age, exceptions & I/O
├── test_interactive_simulation.py # End-to-end simulated CLI interaction test
├── students.txt                   # Data persistence file (openable in Notepad)
└── README.md                      # Documentation & instructions
```

---

## How to Run

### 1. Run the Application
From PowerShell or Command Prompt:

```powershell
python student_manager.py
```

### 2. Main Menu Options
```text
=============================================
      STUDENT RECORD MANAGER (Module 2)
=============================================
1. Add Student
2. View All Students
3. Search Student by ID
4. Open Records File in Notepad
5. Exit
=============================================
```

- **Option 1**: Prompts you step-by-step for student details. If an invalid value is entered (e.g. an age like `abc` or `-5`, or an email like `not_an_email`), the system catches the exception and prompts you again without crashing.
- **Option 2**: Reads and lists all records saved in `students.txt`.
- **Option 3**: Looks up an individual student by ID.
- **Option 4**: Directly opens `students.txt` in **Windows Notepad**.
- **Option 5**: Exits cleanly.

---

## Running the Automated Unit Tests

To run all automated tests verifying email regex, input validation, and file I/O:

```powershell
python -m unittest discover
```
