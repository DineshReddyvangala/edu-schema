# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import script  # Importing our database script

def main():
    root = tk.Tk()
    root.title("EduSchema Management System")
    root.geometry("800x600")

    tab_control = ttk.Notebook(root)

    # Define tabs
    tabs = [
        ("Courses", add_course_management),
        ("Instructors", add_instructor_management),
        ("Students", add_student_management),
        ("Enrollments", add_enrollment_management),
        ("Assignments", add_assignment_management),
        ("Grades", add_grade_management),
        ("Deleted Entities", add_deleted_entities_management)
    ]

    for tab_name, tab_func in tabs:
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=tab_name)
        tab_func(tab)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()

def add_course_management(tab):
    create_management_ui(tab, "Course", ["Course Name", "Course Description", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
                         ["courseName", "courseDescription", "startDate", "endDate"], "courseID")

def add_instructor_management(tab):
    create_management_ui(tab, "Instructor", ["First Name", "Last Name", "Email", "Phone"],
                         ["firstName", "lastName", "email", "phone"], "instructorID")

def add_student_management(tab):
    create_management_ui(tab, "Student", ["First Name", "Last Name", "Email", "Phone"],
                         ["firstName", "lastName", "email", "phone"], "studentID")

def add_enrollment_management(tab):
    create_management_ui(tab, "Enrollment", ["Student ID", "Course ID"],
                         ["studentID", "courseID"], "enrollmentID")

def add_assignment_management(tab):
    create_management_ui(tab, "Assignment", ["Assignment Name", "Due Date (YYYY-MM-DD)"],
                         ["assignmentName", "dueDate"], "assignmentID")

def add_grade_management(tab):
    create_management_ui(tab, "Grade", ["Student ID", "Assignment ID", "Grade"],
                         ["studentID", "assignmentID", "grade"], "gradeID")

def add_deleted_entities_management(tab):
    columns = ("entity_type", "entity_id", "deleted_at")
    treeview = ttk.Treeview(tab, columns=columns, show="headings")

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)

    treeview.grid(row=0, column=0, sticky="nsew")

    def refresh_deleted_entities():
        for item in treeview.get_children():
            treeview.delete(item)

        connection = script.create_connection()
        if connection:
            query = "SELECT entity_type, entity_id, deleted_at FROM deleted_entities"
            records = script.fetch_data(connection, query)
            if records:
                for row in records:
                    treeview.insert("", "end", values=row)
            script.close_connection(connection)

    refresh_button = tk.Button(tab, text="Refresh", command=refresh_deleted_entities)
    refresh_button.grid(row=1, column=0, pady=10)

def create_management_ui(tab, entity_name, labels, db_fields, id_field):
    entries = {}

    for idx, label_text in enumerate(labels):
        tk.Label(tab, text=f"{label_text}:").grid(row=idx, column=0, padx=10, pady=10)
        entry = tk.Entry(tab)
        entry.grid(row=idx, column=1, padx=10, pady=10)
        entries[db_fields[idx]] = entry

    def add_entity():
        values = {field: entry.get() for field, entry in entries.items()}
        connection = script.create_connection()
        if connection:
            query = f"INSERT INTO {entity_name}s ({', '.join(db_fields)}) VALUES ({', '.join(['%s'] * len(db_fields))})"
            success = script.execute_query(connection, query, tuple(values.values()))
            script.close_connection(connection)

            if success:
                messagebox.showinfo("Success", f"{entity_name} added successfully")
            else:
                messagebox.showerror("Error", f"Failed to add {entity_name}")

    def delete_entity():
        entity_id = entry_id.get()
        if not entity_id:
            messagebox.showerror("Input Error", f"{entity_name} ID is required")
            return

        connection = script.create_connection()
        if connection:
            query = f"DELETE FROM {entity_name}s WHERE {id_field} = %s"
            success = script.execute_query(connection, query, (entity_id,))
            if success:
                script.log_deletion(entity_name, entity_id)
                messagebox.showinfo("Success", f"{entity_name} deleted successfully")
            else:
                messagebox.showerror("Error", f"Failed to delete {entity_name}")
            script.close_connection(connection)

    tk.Button(tab, text=f"Add {entity_name}", command=add_entity).grid(row=len(labels), column=0, columnspan=2, pady=20)
    tk.Label(tab, text=f"{entity_name} ID to Delete:").grid(row=len(labels) + 1, column=0, padx=10, pady=10)
    entry_id = tk.Entry(tab)
    entry_id.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
    tk.Button(tab, text=f"Delete {entity_name}", command=delete_entity).grid(row=len(labels) + 2, column=0, columnspan=2, pady=20)

# Start the application
if __name__ == "__main__":
    main()
