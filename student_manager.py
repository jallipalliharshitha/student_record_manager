"""
Student Record Manager
Module 2 Assignment

Features:
- Add Student
- Validate Email using Regular Expressions (Regex)
- Save Data to File (Notepad-compatible text format)
- Read Student Data from File
- Handle Invalid Input using Built-in and Custom Exceptions
- Direct option to view/open records in Notepad
"""

import os
import re
import sys
import subprocess
from typing import List, Optional


# ==========================================
# Custom Exception Classes
# ==========================================

class InvalidEmailError(ValueError):
    """Raised when an email address does not match the valid regex format."""
    pass


class InvalidAgeError(ValueError):
    """Raised when an entered age is outside a realistic or valid range."""
    pass


class DuplicateStudentError(Exception):
    """Raised when attempting to add a student whose ID already exists."""
    pass


class StudentNotFoundError(Exception):
    """Raised when searching for a student ID that does not exist in records."""
    pass


# ==========================================
# Student Model
# ==========================================

class Student:
    """Represents a student record."""

    def __init__(self, student_id: str, name: str, age: int, course: str, email: str):
        self.student_id = student_id.strip()
        self.name = name.strip()
        self.age = age
        self.course = course.strip()
        self.email = email.strip()

    def to_file_line(self) -> str:
        """Serializes the student record into a clean pipe-delimited line for text files."""
        return f"{self.student_id} | {self.name} | {self.age} | {self.course} | {self.email}\n"

    @classmethod
    def from_file_line(cls, line: str) -> Optional["Student"]:
        """
        Parses a line from the text file into a Student instance.
        Gracefully skips headers, decorative lines, or malformed entries.
        """
        line = line.strip()
        if not line or line.startswith("=") or line.startswith("#") or line.startswith("---"):
            return None

        parts = [part.strip() for part in line.split("|")]
        if len(parts) == 5:
            student_id, name, age_str, course, email = parts
            # Check that age is a valid integer, otherwise treat as header line
            try:
                age = int(age_str)
                return cls(student_id, name, age, course, email)
            except ValueError:
                return None
        return None

    def display(self) -> str:
        """Returns a formatted string representing the student."""
        return (
            f"ID     : {self.student_id}\n"
            f"Name   : {self.name}\n"
            f"Age    : {self.age}\n"
            f"Course : {self.course}\n"
            f"Email  : {self.email}"
        )


# ==========================================
# Validation Functions
# ==========================================

# Regex pattern for validating standard email addresses
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"


def validate_email(email: str) -> bool:
    """
    Validates email format using regex.
    Raises InvalidEmailError if invalid.
    """
    cleaned_email = email.strip()
    if not cleaned_email or not re.match(EMAIL_REGEX, cleaned_email):
        raise InvalidEmailError(
            f"'{email}' is not a valid email address. Format must be like username@domain.com"
        )
    return True


def validate_age(age_val: int) -> bool:
    """
    Validates that age is a reasonable positive number.
    Raises InvalidAgeError if invalid.
    """
    if age_val < 5 or age_val > 120:
        raise InvalidAgeError(f"Age must be between 5 and 120 (entered: {age_val}).")
    return True


# ==========================================
# File I/O Functions (Notepad Compatible)
# ==========================================

DEFAULT_FILE = "students.txt"
FILE_HEADER = (
    "========================================================================================\n"
    "STUDENT RECORDS (Opened via Notepad)\n"
    "Format: STUDENT ID | NAME | AGE | COURSE | EMAIL\n"
    "========================================================================================\n"
)


def ensure_file_initialized(filename: Optional[str] = None) -> str:
    """Ensures the text file exists with a friendly header for Notepad viewing."""
    target_file = filename if filename is not None else DEFAULT_FILE
    if not os.path.exists(target_file) or os.path.getsize(target_file) == 0:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(FILE_HEADER)
    return target_file


def read_students_from_file(filename: Optional[str] = None) -> List[Student]:
    """
    Reads all student records from the text file.
    Handles FileNotFoundError if the file does not exist.
    """
    target_file = filename if filename is not None else DEFAULT_FILE
    if not os.path.exists(target_file):
        return []

    students: List[Student] = []
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            for line in f:
                student = Student.from_file_line(line)
                if student:
                    students.append(student)
    except Exception as e:
        print(f"[Error reading file]: {e}")

    return students


def save_student_to_file(student: Student, filename: Optional[str] = None) -> None:
    """
    Appends a new student record to the text file.
    Ensures headers exist so opening in Notepad is clean and readable.
    """
    target_file = ensure_file_initialized(filename)
    with open(target_file, "a", encoding="utf-8") as f:
        f.write(student.to_file_line())


def open_file_in_notepad(filename: Optional[str] = None) -> None:
    """
    Opens the text file directly in Windows Notepad so the user can inspect it.
    """
    target_file = ensure_file_initialized(filename)
    abs_path = os.path.abspath(target_file)
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen(["notepad.exe", abs_path])
            print(f"[Success] Opened '{abs_path}' in Notepad.")
        else:
            print(f"[Info] Notepad is Windows-only. File saved at: {abs_path}")
    except Exception as e:
        print(f"[Error opening Notepad]: {e}")


# ==========================================
# Interactive User Input Handlers
# ==========================================

def prompt_student_id(existing_ids: set) -> str:
    """Prompts for student ID and handles empty/duplicate validation."""
    while True:
        try:
            student_id = input("Enter Student ID (e.g., S101): ").strip().upper()
            if not student_id:
                raise ValueError("Student ID cannot be empty.")
            if student_id in existing_ids:
                raise DuplicateStudentError(f"Student ID '{student_id}' already exists!")
            return student_id
        except (ValueError, DuplicateStudentError) as e:
            print(f"  [Input Error] {e} Please try again.\n")


def prompt_student_name() -> str:
    """Prompts for student name and handles validation."""
    while True:
        try:
            name = input("Enter Student Full Name: ").strip()
            if not name:
                raise ValueError("Student name cannot be empty.")
            if any(char.isdigit() for char in name):
                raise ValueError("Student name should not contain numbers.")
            return name
        except ValueError as e:
            print(f"  [Input Error] {e} Please try again.\n")


def prompt_student_age() -> int:
    """Prompts for age and handles invalid format/range exceptions."""
    while True:
        try:
            raw_age = input("Enter Age (integer): ").strip()
            if not raw_age:
                raise ValueError("Age cannot be empty.")
            age = int(raw_age)
            validate_age(age)
            return age
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("  [Input Error] Age must be a numeric integer. Please try again.\n")
            else:
                print(f"  [Input Error] {e} Please try again.\n")
        except InvalidAgeError as e:
            print(f"  [Validation Error] {e} Please try again.\n")


def prompt_student_course() -> str:
    """Prompts for course name and validates non-empty."""
    while True:
        try:
            course = input("Enter Course / Program: ").strip()
            if not course:
                raise ValueError("Course cannot be empty.")
            return course
        except ValueError as e:
            print(f"  [Input Error] {e} Please try again.\n")


def prompt_student_email() -> str:
    """Prompts for email and validates using regex."""
    while True:
        try:
            email = input("Enter Student Email (e.g., student@domain.com): ").strip()
            validate_email(email)
            return email
        except InvalidEmailError as e:
            print(f"  [Validation Error] {e} Please try again.\n")


# ==========================================
# Main Menu Operations
# ==========================================

def add_student_flow(filename: Optional[str] = None) -> None:
    """Collects student details, validates each field, and appends to file."""
    target_file = filename if filename is not None else DEFAULT_FILE
    print("\n--- ADD NEW STUDENT ---")
    current_students = read_students_from_file(target_file)
    existing_ids = {s.student_id for s in current_students}

    student_id = prompt_student_id(existing_ids)
    name = prompt_student_name()
    age = prompt_student_age()
    course = prompt_student_course()
    email = prompt_student_email()

    student = Student(student_id, name, age, course, email)
    save_student_to_file(student, target_file)
    print(f"\n[Success] Student '{name}' (ID: {student_id}) saved successfully to '{target_file}'!")


def view_students_flow(filename: Optional[str] = None) -> None:
    """Reads and displays all student records from the text file."""
    target_file = filename if filename is not None else DEFAULT_FILE
    print("\n--- VIEW ALL STUDENTS ---")
    students = read_students_from_file(target_file)

    if not students:
        print("No student records found in file. Choose option 1 to add a student.")
        return

    print(f"Total Records Found: {len(students)}\n")
    header = f"{'ID':<10} | {'Name':<22} | {'Age':<5} | {'Course':<20} | {'Email':<30}"
    print(header)
    print("-" * len(header))
    for s in students:
        print(f"{s.student_id:<10} | {s.name:<22} | {s.age:<5} | {s.course:<20} | {s.email:<30}")
    print("-" * len(header))


def search_student_flow(filename: Optional[str] = None) -> None:
    """Searches for a student by ID."""
    target_file = filename if filename is not None else DEFAULT_FILE
    print("\n--- SEARCH STUDENT BY ID ---")
    students = read_students_from_file(target_file)
    if not students:
        print("No student records found in file.")
        return

    try:
        search_id = input("Enter Student ID to search: ").strip().upper()
        if not search_id:
            raise ValueError("Search ID cannot be empty.")

        matched = next((s for s in students if s.student_id == search_id), None)
        if not matched:
            raise StudentNotFoundError(f"No student found with ID '{search_id}'.")

        print("\n[Student Found]")
        print(matched.display())
    except (ValueError, StudentNotFoundError) as e:
        print(f"[Search Notice] {e}")


def display_menu() -> None:
    """Displays the main CLI menu."""
    print("\n" + "=" * 45)
    print("      STUDENT RECORD MANAGER (Module 2)")
    print("=" * 45)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student by ID")
    print("4. Open Records File in Notepad")
    print("5. Exit")
    print("=" * 45)


def main() -> None:
    """Main program execution loop."""
    print("Welcome to Student Record Manager!")
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student_flow()
        elif choice == "2":
            view_students_flow()
        elif choice == "3":
            search_student_flow()
        elif choice == "4":
            open_file_in_notepad()
        elif choice == "5":
            print("\nThank you for using Student Record Manager. Goodbye!")
            break
        else:
            print("\n[Invalid Selection] Please choose a valid number between 1 and 5.")


if __name__ == "__main__":
    main()
