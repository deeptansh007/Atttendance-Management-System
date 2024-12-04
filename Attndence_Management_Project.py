import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import datetime

class AttendanceManagementSystem:
    def __init__(self, root):  # Corrected constructor name
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("600x400")
        
        # Data structures to hold students and attendance
        self.students = []
        self.attendance_data = {}
        
        # Load existing data if available
        self.load_data()
        
        # Create GUI Components
        self.create_widgets()

    def create_widgets(self):
        """Create the components of the GUI."""
        
        # Title Label
        self.title_label = tk.Label(self.root, text="Attendance Management System", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Buttons
        self.add_student_button = tk.Button(self.root, text="Add Student", command=self.add_student, width=20)
        self.add_student_button.pack(pady=5)

        self.mark_attendance_button = tk.Button(self.root, text="Mark Attendance", command=self.mark_attendance, width=20)
        self.mark_attendance_button.pack(pady=5)

        self.view_attendance_button = tk.Button(self.root, text="View Attendance", command=self.view_attendance, width=20)
        self.view_attendance_button.pack(pady=5)

        self.view_student_attendance_button = tk.Button(self.root, text="View Student's Attendance", command=self.view_student_attendance, width=20)
        self.view_student_attendance_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program, width=20)
        self.exit_button.pack(pady=20)

    def add_student(self):
        """Add a new student to the system."""
        student_name = simpledialog.askstring("Input", "Enter student's name:", parent=self.root)
        
        if student_name and student_name not in self.students:
            self.students.append(student_name)
            self.attendance_data[student_name] = []
            messagebox.showinfo("Success", f"Student {student_name} added successfully!")
        elif student_name in self.students:
            messagebox.showwarning("Warning", f"Student {student_name} already exists.")
        else:
            messagebox.showwarning("Warning", "Name cannot be empty.")

    def mark_attendance(self):
        """Mark attendance for all students."""
        date = datetime.date.today().strftime("%Y-%m-%d")
        for student in self.students:
            status = simpledialog.askstring("Attendance", f"Is {student} present? (y/n):", parent=self.root)
            if status and status.lower() == "y":
                self.attendance_data[student].append((date, 'Present'))
            else:
                self.attendance_data[student].append((date, 'Absent'))
        
        messagebox.showinfo("Success", "Attendance marked successfully.")

    def view_attendance(self):
        """View the attendance of all students."""
        attendance_window = tk.Toplevel(self.root)
        attendance_window.title("View Attendance")
        attendance_window.geometry("500x400")

        text = tk.Text(attendance_window, width=60, height=20)
        text.pack(pady=10)
        
        for student, records in self.attendance_data.items():
            text.insert(tk.END, f"{student}:\n")
            for record in records:
                text.insert(tk.END, f"  {record[0]}: {record[1]}\n")
            text.insert(tk.END, "\n")

    def view_student_attendance(self):
        """View the attendance for a specific student."""
        student_name = simpledialog.askstring("Input", "Enter the student's name:", parent=self.root)
        
        if student_name and student_name in self.attendance_data:
            attendance_window = tk.Toplevel(self.root)
            attendance_window.title(f"Attendance for {student_name}")
            attendance_window.geometry("500x400")
            
            text = tk.Text(attendance_window, width=60, height=20)
            text.pack(pady=10)
            
            text.insert(tk.END, f"Attendance records for {student_name}:\n")
            for record in self.attendance_data[student_name]:
                text.insert(tk.END, f"  {record[0]}: {record[1]}\n")
        elif student_name not in self.attendance_data:
            messagebox.showwarning("Warning", f"Student {student_name} not found.")
        else:
            messagebox.showwarning("Warning", "Name cannot be empty.")

    def load_data(self):
        """Load attendance data from file."""
        try:
            with open("attendance.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        student_name = parts[0]
                        attendance = eval(parts[1])  # Convert the string back to a list
                        self.attendance_data[student_name] = attendance
                        self.students.append(student_name)
        except FileNotFoundError:
            pass

    def save_data(self):
        """Save attendance data to file."""
        with open("attendance.txt", "w") as file:
            for student in self.students:
                attendance = self.attendance_data.get(student, [])
                file.write(f"{student},{attendance}\n")

    def exit_program(self):
        """Exit the program and save data."""
        self.save_data()
        self.root.quit()


# Run the application
if __name__ == "__main__":  # Corrected here
    root = tk.Tk()
    system = AttendanceManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", system.exit_program)
    root.mainloop()
