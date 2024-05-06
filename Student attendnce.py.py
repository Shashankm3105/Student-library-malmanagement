import mysql.connector
import tkinter as tk
from tkinter import ttk

class Student:
    def __init__(self, roll_no, name):
        self.roll_no = roll_no
        self.name = name
        self.attendance = {}

    def mark_attendance(self, date, status):
        self.attendance[date] = status

    def get_attendance(self):
        return self.attendance


class AttendanceManager:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Students (
                                roll_no VARCHAR(255) PRIMARY KEY,
                                name VARCHAR(255)
                            )''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Attendance (
                                roll_no VARCHAR(255),
                                date DATE,
                                status VARCHAR(255),
                                FOREIGN KEY(roll_no) REFERENCES Students(roll_no)
                            )''')
        self.conn.commit()

    def add_student(self, roll_no, name):
        self.cur.execute("INSERT INTO Students VALUES (%s, %s)", (roll_no, name))
        self.conn.commit()
        return f"Student {name} added successfully."

    def delete_student(self, roll_no):
        self.cur.execute("DELETE FROM Students WHERE roll_no=%s", (roll_no,))
        self.conn.commit()
        return f"Student with Roll No: {roll_no} deleted successfully."

    def mark_attendance(self, roll_no, date, status):
        self.cur.execute("INSERT INTO Attendance VALUES (%s, %s, %s)", (roll_no, date, status))
        self.conn.commit()
        return f"Attendance marked for roll number {roll_no} on {date}."

    def view_attendance(self, roll_no):
        self.cur.execute("SELECT date, status FROM Attendance WHERE roll_no=%s", (roll_no,))
        attendance_records = self.cur.fetchall()
        if attendance_records:
            attendance_text = f"Attendance for student with roll number {roll_no}:\n"
            for record in attendance_records:
                attendance_text += f"{record[0]}: {record[1]}\n"
            return attendance_text
        else:
            return "No attendance records found for this student."

    def view_students_data(self):
        self.cur.execute("SELECT * FROM Students")
        students_list = self.cur.fetchall()
        return students_list

    def get_student_attendance(self, roll_no):
        self.cur.execute("SELECT date, status FROM Attendance WHERE roll_no=%s", (roll_no,))
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()


def add_student_gui(attendance_manager):
    def submit():
        roll_no = roll_no_entry.get()
        name = name_entry.get()
        result_label.config(text=attendance_manager.add_student(roll_no, name))
        roll_no_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Add Student")
    root.geometry("300x150")

    roll_no_label = tk.Label(root, text="Roll Number:")
    roll_no_label.pack()

    roll_no_entry = tk.Entry(root)
    roll_no_entry.pack()

    name_label = tk.Label(root, text="Name:")
    name_label.pack()

    name_entry = tk.Entry(root)
    name_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()


def delete_student_gui(attendance_manager):
    def submit():
        roll_no = roll_no_entry.get()
        result_label.config(text=attendance_manager.delete_student(roll_no))
        roll_no_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Delete Student")
    root.geometry("300x100")

    roll_no_label = tk.Label(root, text="Enter Roll Number to Delete:")
    roll_no_label.pack()

    roll_no_entry = tk.Entry(root)
    roll_no_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()


def mark_attendance_gui(attendance_manager):
    def submit():
        roll_no = roll_no_entry.get()
        date = date_entry.get()
        status = status_var.get()
        result_label.config(text=attendance_manager.mark_attendance(roll_no, date, status))
        roll_no_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Mark Attendance")
    root.geometry("300x200")

    roll_no_label = tk.Label(root, text="Roll Number:")
    roll_no_label.pack()

    roll_no_entry = tk.Entry(root)
    roll_no_entry.pack()

    date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
    date_label.pack()

    date_entry = tk.Entry(root)
    date_entry.pack()

    status_label = tk.Label(root, text="Status:")
    status_label.pack()

    status_var = tk.StringVar(root)
    status_var.set("Present")

    status_options = ["Present", "Absent"]
    status_menu = tk.OptionMenu(root, status_var, *status_options)
    status_menu.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()


def view_attendance_gui(attendance_manager):
    def submit():
        roll_no = roll_no_entry.get()
        result_text = attendance_manager.view_attendance(roll_no)
        result_text_widget.config(state=tk.NORMAL)
        result_text_widget.delete(1.0, tk.END)
        result_text_widget.insert(tk.END, result_text)
        result_text_widget.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("View Attendance")
    root.geometry("300x200")

    roll_no_label = tk.Label(root, text="Roll Number:")
    roll_no_label.pack()

    roll_no_entry = tk.Entry(root)
    roll_no_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    result_text_widget = tk.Text(root, height=8, width=30)
    result_text_widget.pack()

    root.mainloop()


def view_students_list_gui(attendance_manager):
    def view_attendance_data(event):
        selected_item = students_treeview.selection()[0]
        roll_no, name = students_treeview.item(selected_item, 'values')
        attendance_data = attendance_manager.get_student_attendance(roll_no)
        attendance_text = f"Roll No: {roll_no}\nName: {name}\n\nDate\t\tStatus\n"
        for record in attendance_data:
            attendance_text += f"{record[0]}\t{record[1]}\n"
        attendance_label.config(text=attendance_text)

    students_data = attendance_manager.view_students_data()

    root = tk.Tk()
    root.title("Students List")
    root.geometry("500x400")
    root.configure(bg='light blue')

    students_treeview = ttk.Treeview(root, columns=("Roll No", "Name"), show="headings")
    students_treeview.heading("Roll No", text="Roll No")
    students_treeview.heading("Name", text="Name")
    students_treeview.pack(expand=True, fill="both")

    for student in students_data:
        students_treeview.insert("", "end", values=student)

    students_treeview.bind("<Double-1>", view_attendance_data)

    attendance_label = tk.Label(root, text="", justify="left")
    attendance_label.pack()

    root.mainloop()


def view_students_data_gui(attendance_manager):
    students_data_text = attendance_manager.view_students_data()

    root = tk.Tk()
    root.title("Students Data")
    root.geometry("500x400")

    students_data_label = tk.Label(root, text=students_data_text, justify="left")
    students_data_label.pack(fill="both", expand=True)

    root.mainloop()


def main():
    host = "localhost"
    user = "root"
    password = "root"
    database = "shashank"

    attendance_manager = AttendanceManager(host, user, password, database)

    root = tk.Tk()
    root.title("Attendance Management System")
    root.geometry("300x400")

    def add_student():
        add_student_gui(attendance_manager)

    def delete_student():
        delete_student_gui(attendance_manager)

    def mark_attendance():
        mark_attendance_gui(attendance_manager)

    def view_attendance():
        view_attendance_gui(attendance_manager)

    def view_students_list():
        view_students_list_gui(attendance_manager)

    def view_students_data():
        view_students_data_gui(attendance_manager)

    def exit_program():
        attendance_manager.close_connection()
        root.destroy()

    add_student_button = tk.Button(root, text="Add Student", command=add_student)
    add_student_button.pack(pady=10)

    delete_student_button = tk.Button(root, text="Delete Student", command=delete_student)
    delete_student_button.pack(pady=10)

    mark_attendance_button = tk.Button(root, text="Mark Attendance", command=mark_attendance)
    mark_attendance_button.pack(pady=10)

    view_attendance_button = tk.Button(root, text="View Attendance", command=view_attendance)
    view_attendance_button.pack(pady=10)

    view_students_list_button = tk.Button(root, text="View Students List", command=view_students_list)
    view_students_list_button.pack(pady=10)

    view_students_data_button = tk.Button(root, text="View Students Data", command=view_students_data)
    view_students_data_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=exit_program)
    exit_button.pack(pady=10)

    root.configure(bg='light blue')
    root.mainloop()


if __name__ == "__main__":
    main()
