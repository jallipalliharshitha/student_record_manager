"""
Unit Tests for Student Record Manager
Module 2 Assignment
"""

import os
import unittest
from student_manager import (
    Student,
    validate_email,
    validate_age,
    InvalidEmailError,
    InvalidAgeError,
    read_students_from_file,
    save_student_to_file,
    ensure_file_initialized
)


class TestStudentRecordManager(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test file for each test case."""
        self.test_filename = "test_students.txt"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        """Clean up test file after test execution."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    # -------------------------------------------------------------
    # 1. Regex Email Validation Tests
    # -------------------------------------------------------------
    def test_valid_emails(self):
        """Test standard valid email formats."""
        valid_emails = [
            "student@example.com",
            "john.doe@university.edu",
            "jane_smith123@college.ac.in",
            "first.last+tag@sub.domain.org"
        ]
        for email in valid_emails:
            self.assertTrue(validate_email(email), f"Failed on valid email: {email}")

    def test_invalid_emails_raise_exception(self):
        """Test that malformed emails properly raise InvalidEmailError."""
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@domain",
            "user@domain..com",
            "user name@domain.com",
            ""
        ]
        for email in invalid_emails:
            with self.assertRaises(InvalidEmailError, msg=f"Should raise for: {email}"):
                validate_email(email)

    # -------------------------------------------------------------
    # 2. Age Validation Tests
    # -------------------------------------------------------------
    def test_valid_age(self):
        """Test valid age boundary conditions."""
        self.assertTrue(validate_age(18))
        self.assertTrue(validate_age(5))
        self.assertTrue(validate_age(120))

    def test_invalid_age_raises_exception(self):
        """Test that invalid age values raise InvalidAgeError."""
        invalid_ages = [-5, 0, 4, 121, 200]
        for age in invalid_ages:
            with self.assertRaises(InvalidAgeError, msg=f"Should raise for age: {age}"):
                validate_age(age)

    # -------------------------------------------------------------
    # 3. Student Serialization and Deserialization
    # -------------------------------------------------------------
    def test_student_to_and_from_line(self):
        """Test serialization to file line and deserialization back to object."""
        student = Student("S101", "Alex Morgan", 21, "Data Science", "alex@example.com")
        line = student.to_file_line()
        self.assertEqual(line, "S101 | Alex Morgan | 21 | Data Science | alex@example.com\n")

        parsed_student = Student.from_file_line(line)
        self.assertIsNotNone(parsed_student)
        self.assertEqual(parsed_student.student_id, "S101")
        self.assertEqual(parsed_student.name, "Alex Morgan")
        self.assertEqual(parsed_student.age, 21)
        self.assertEqual(parsed_student.course, "Data Science")
        self.assertEqual(parsed_student.email, "alex@example.com")

    # -------------------------------------------------------------
    # 4. File I/O Persistence (Notepad format)
    # -------------------------------------------------------------
    def test_save_and_read_file(self):
        """Test writing to file and reading back student records."""
        ensure_file_initialized(self.test_filename)
        
        student1 = Student("S101", "Alice Smith", 20, "Computer Science", "alice@test.com")
        student2 = Student("S102", "Bob Jones", 22, "Information Technology", "bob@test.com")

        save_student_to_file(student1, self.test_filename)
        save_student_to_file(student2, self.test_filename)

        loaded_students = read_students_from_file(self.test_filename)
        self.assertEqual(len(loaded_students), 2)
        self.assertEqual(loaded_students[0].student_id, "S101")
        self.assertEqual(loaded_students[0].name, "Alice Smith")
        self.assertEqual(loaded_students[1].student_id, "S102")
        self.assertEqual(loaded_students[1].name, "Bob Jones")

    def test_empty_file_handling(self):
        """Test that reading a non-existent file returns an empty list without error."""
        records = read_students_from_file("non_existent_file.txt")
        self.assertEqual(records, [])


if __name__ == "__main__":
    unittest.main()
