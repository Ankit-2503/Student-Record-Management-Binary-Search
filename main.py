"""
Student Record Management System Using Binary Search
Subject: Design and Analysis of Algorithms (DAA)
Language: Python 3
Interface: Tkinter GUI

Run:
    python main.py

The records are kept sorted by student ID. Binary Search is used to find
a student efficiently. Data is saved in students.json in the same folder.
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")


def load_students():
    """Load saved records. Return an empty list if no file exists."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return sorted(data, key=lambda student: student["id"].casefold())
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        messagebox.showwarning(
            "Data warning",
            "The saved data could not be read. Starting with an empty list."
        )
        return []


def save_students(students):
    """Save all student records to a JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def binary_search(students: list[dict], student_id: str) -> int:
    """Return the matching index in an ID-sorted list, or -1 if absent."""
    target = student_id.casefold()
    low, high = 0, len(students) - 1

    while low <= high:
        middle = (low + high) // 2
        current_id = students[middle]["id"].casefold()

        if current_id == target:
            return middle
        elif current_id < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("900x600")
        self.root.minsize(760, 520)
        self.students = load_students()

        self.setup_style()
        self.create_widgets()
        self.refresh_table()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))

    def create_widgets(self):
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer,
            text="Student Record Management System",
            style="Title.TLabel"
        ).pack(pady=(0, 4))

        ttk.Label(
            outer,
            text="Using Binary Search Algorithm",
            font=("Arial", 11)
        ).pack(pady=(0, 16))

        form = ttk.LabelFrame(outer, text="Student Details", padding=12)
        form.pack(fill="x", pady=5)

        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.email_var = tk.StringVar()

        fields = [
            ("Student ID", self.id_var),
            ("Student Name", self.name_var),
            ("Course", self.course_var),
            ("Email", self.email_var),
        ]

        for index, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(
                row=0, column=index, sticky="w", padx=5, pady=(0, 5)
            )
            ttk.Entry(form, textvariable=variable, width=22).grid(
                row=1, column=index, sticky="ew", padx=5, pady=(0, 5)
            )
            form.columnconfigure(index, weight=1)

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=10)

        ttk.Button(buttons, text="Add Student", command=self.add_student).pack(
            side="left", padx=4
        )
        ttk.Button(buttons, text="Search (Binary Search)",
                   command=self.search_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Selected",
                   command=self.update_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete Selected",
                   command=self.delete_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear Fields",
                   command=self.clear_fields).pack(side="left", padx=4)
        ttk.Button(buttons, text="Show All",
                   command=self.refresh_table).pack(side="right", padx=4)

        search_frame = ttk.Frame(outer)
        search_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(search_frame, text="Search by Student ID:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=25).pack(
            side="left", padx=8
        )
        ttk.Button(search_frame, text="Find",
                   command=self.search_student).pack(side="left")

        table_frame = ttk.LabelFrame(outer, text="Student Records", padding=8)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "course", "email")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("course", text="Course")
        self.tree.heading("email", text="Email")
        self.tree.column("id", width=110, anchor="center")
        self.tree.column("name", width=210)
        self.tree.column("course", width=140, anchor="center")
        self.tree.column("email", width=250)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(outer, textvariable=self.status_var).pack(
            anchor="w", pady=(8, 0)
        )

    def validate_fields(self):
        student_id = self.id_var.get().strip()
        name = self.name_var.get().strip()
        course = self.course_var.get().strip()
        email = self.email_var.get().strip()

        if not student_id or not name or not course:
            messagebox.showerror(
                "Missing details",
                "Please enter Student ID, Student Name, and Course."
            )
            return None

        return {
            "id": student_id,
            "name": name,
            "course": course,
            "email": email
        }

    def sort_records(self):
        self.students.sort(key=lambda student: student["id"].casefold())

    def add_student(self):
        record = self.validate_fields()
        if record is None:
            return

        if binary_search(self.students, record["id"]) != -1:
            messagebox.showerror("Duplicate ID", "This Student ID already exists.")
            return

        self.students.append(record)
        self.sort_records()
        self.persist_and_refresh()
        self.clear_fields()
        self.status_var.set(f"Student {record['id']} added successfully.")

    def search_student(self):
        student_id = self.search_var.get().strip() or self.id_var.get().strip()
        if not student_id:
            messagebox.showinfo("Search", "Enter a Student ID to search.")
            return

        # Binary Search is performed on the ID-sorted student list.
        index = binary_search(self.students, student_id)

        if index == -1:
            messagebox.showinfo("Not found", f"No student found with ID {student_id}.")
            self.status_var.set("Search completed: record not found.")
            return

        student = self.students[index]
        self.id_var.set(student["id"])
        self.name_var.set(student["name"])
        self.course_var.set(student["course"])
        self.email_var.set(student.get("email", ""))

        self.refresh_table(selected_id=student["id"])
        self.status_var.set(
            f"Found {student['name']} at list index {index} using Binary Search."
        )
        messagebox.showinfo(
            "Student Found",
            f"Student ID: {student['id']}\n"
            f"Name: {student['name']}\n"
            f"Course: {student['course']}\n"
            f"Email: {student.get('email', '')}\n\n"
            f"Binary Search index: {index}"
        )

    def selected_student_id(self):
        selection = self.tree.selection()
        if not selection:
            return None
        values = self.tree.item(selection[0], "values")
        return values[0] if values else None

    def update_student(self):
        old_id = self.selected_student_id()
        if old_id is None:
            messagebox.showinfo("Update", "Select a student record from the table.")
            return

        record = self.validate_fields()
        if record is None:
            return

        old_index = binary_search(self.students, old_id)
        if old_index == -1:
            messagebox.showerror("Error", "Selected record was not found.")
            return

        new_index = binary_search(self.students, record["id"])
        if new_index != -1 and record["id"].casefold() != old_id.casefold():
            messagebox.showerror("Duplicate ID", "Another student already uses this ID.")
            return

        self.students[old_index] = record
        self.sort_records()
        self.persist_and_refresh()
        self.clear_fields()
        self.status_var.set(f"Student {record['id']} updated successfully.")

    def delete_student(self):
        student_id = self.selected_student_id()
        if student_id is None:
            messagebox.showinfo("Delete", "Select a student record from the table.")
            return

        index = binary_search(self.students, student_id)
        if index == -1:
            messagebox.showerror("Error", "Selected record was not found.")
            return

        if messagebox.askyesno(
            "Confirm delete", f"Delete student {student_id}?"
        ):
            del self.students[index]
            self.persist_and_refresh()
            self.clear_fields()
            self.status_var.set(f"Student {student_id} deleted.")

    def on_select(self, _event):
        student_id = self.selected_student_id()
        if student_id is None:
            return
        index = binary_search(self.students, student_id)
        if index != -1:
            student = self.students[index]
            self.id_var.set(student["id"])
            self.name_var.set(student["name"])
            self.course_var.set(student["course"])
            self.email_var.set(student.get("email", ""))

    def refresh_table(self, selected_id=None):
        self.sort_records()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student in self.students:
            item = self.tree.insert(
                "", "end",
                values=(
                    student["id"],
                    student["name"],
                    student["course"],
                    student.get("email", "")
                )
            )
            if selected_id and student["id"].casefold() == selected_id.casefold():
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)

        self.status_var.set(f"Total student records: {len(self.students)}")

    def persist_and_refresh(self):
        try:
            save_students(self.students)
        except OSError as error:
            messagebox.showerror("Save error", f"Could not save data:\n{error}")
        self.refresh_table()

    def clear_fields(self):
        self.id_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.email_var.set("")
        self.search_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
