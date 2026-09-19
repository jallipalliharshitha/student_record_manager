"""
Simulated Interactive Flow Test for student_manager.py
Tests:
- Menu navigation
- Invalid age input recovered by exception handling
- Invalid email input recovered by regex validation exception handling
- Duplicate ID handling
- Adding valid student
- Reading records from file
- Searching student by ID
"""

import os
import io
import sys
import unittest
from unittest.mock import patch
import student_manager


class TestInteractiveFlow(unittest.TestCase):

    def setUp(self):
        self.filename = "simulated_students.txt"
        student_manager.DEFAULT_FILE = self.filename
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_full_interactive_workflow(self):
        # Sequence of inputs simulated for CLI:
        # 1: Add student
        #    ID: "s101"
        #    Name: "Jane Doe"
        #    Age: "not_a_number" (triggers ValueError), "-10" (triggers InvalidAgeError), "21" (valid)
        #    Course: "Computer Engineering"
        #    Email: "bad_email" (triggers InvalidEmailError), "jane.doe@example.edu" (valid)
        # 1: Try to add student with duplicate ID
        #    ID: "S101" (triggers DuplicateStudentError), "S102"
        #    Name: "Mark Evans"
        #    Age: "22"
        #    Course: "Cybersecurity"
        #    Email: "mark@example.com"
        # 2: View all students
        # 3: Search student by ID -> "S101"
        # 5: Exit
        simulated_inputs = [
            # First student addition
            "1",
            "s101",
            "Jane Doe",
            "not_a_number",   # should trigger ValueError
            "-10",            # should trigger InvalidAgeError
            "21",             # valid age
            "Computer Engineering",
            "bad_email",      # should trigger InvalidEmailError
            "jane.doe@example.edu",
            
            # Second student addition (with duplicate ID attempt)
            "1",
            "S101",           # Duplicate ID
            "S102",           # Valid new ID
            "Mark Evans",
            "22",
            "Cybersecurity",
            "mark@example.com",
            
            # View all students
            "2",
            
            # Search by ID
            "3",
            "S101",
            
            # Exit
            "5"
        ]

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                student_manager.main()
                output = fake_out.getvalue()

        # Assertions
        self.assertIn("Age must be a numeric integer", output)
        self.assertIn("Age must be between 5 and 120", output)
        self.assertIn("is not a valid email address", output)
        self.assertIn("Student ID 'S101' already exists", output)
        self.assertIn("Student 'Jane Doe' (ID: S101) saved successfully", output)
        self.assertIn("Student 'Mark Evans' (ID: S102) saved successfully", output)
        self.assertIn("Total Records Found: 2", output)
        self.assertIn("Jane Doe", output)
        self.assertIn("Mark Evans", output)
        self.assertIn("[Student Found]", output)
        self.assertIn("jane.doe@example.edu", output)

        # Check the text file content
        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("STUDENT RECORDS (Opened via Notepad)", content)
        self.assertIn("S101 | Jane Doe | 21 | Computer Engineering | jane.doe@example.edu", content)
        self.assertIn("S102 | Mark Evans | 22 | Cybersecurity | mark@example.com", content)


if __name__ == "__main__":
    unittest.main()
