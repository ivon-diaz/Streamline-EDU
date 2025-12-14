import tkinter as tk
from tkinter import ttk, messagebox, Canvas, scrolledtext
from datetime import datetime, timedelta, date
from google import genai

# AI KEY (Requires newly generated key to use)
client = genai.Client(api_key="YOUR KEY HERE")


# ========  Login Screen ========
class LoginScreen(tk.Frame):
    def __init__(self, root, login_callback):
        super().__init__(root, bg="#f5f5f5")
        self.root = root
        self.login_callback = login_callback

        self.loginTitle = tk.Label(self,
                          text="Streamline EDU",
                          font=("Arial", 22, "bold"),
                          bg="#f5f5f5",
                          fg="#2196f3",
                          pady=20)
    
        self.loginTitle.pack(fill="x")
    
        self.loginForm = tk.Frame(self,
                         bg="#f5f5f5")
        self.loginForm.pack(pady=60)

        self.usernameLabel = tk.Label(self.loginForm,
                          text="Username",
                          font=("Arial", 13),
                          bg="#f5f5f5")
        self.usernameLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    
        self.usernameEntry = tk.Entry(self.loginForm, 
                             font=("Arial", 13),
                             width=25)
        self.usernameEntry.grid(row=0, column=1, pady=10)

        self.passwordLabel = tk.Label(self.loginForm,
                          text="Password",
                          font=("Arial", 13),
                          bg="#f5f5f5")
        self.passwordLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.passwordEntry = tk.Entry(self.loginForm, 
                             font=("Arial", 13),
                             width=25)
        self.passwordEntry.grid(row=1, column=1, pady=10)

        self.loginButton = tk.Button(self,
                            text="Login",
                            font=("Arial", 14, "bold"),
                            bg="#2196f3",
                            fg="#f5f5f5",
                            relief="flat",
                            padx=30,
                            pady=10,
                            cursor="hand2",
                            command=self.loginValidation)
        self.loginButton.pack(pady=20)

        self.usernameEntry.bind("<Return>", lambda e: self.loginValidation())
        self.passwordEntry.bind("<Return>", lambda e: self.loginValidation())

    def loginValidation(self):
        """Validates user login (preset for test)"""
        userid = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if userid == "username" and password == "password":
            self.login_callback()
        else:
            messagebox.showerror("Login Error", "Incorrect username or password. Please try again")

    def show(self):
        self.pack(fill="both", expand=True)
        self.usernameEntry.focus_set()
    def hide(self):
        self.pack_forget()

# ========= Data Classes for Attendance =========
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

class AttendanceRecord:
    def __init__(self, student_id, date, present: bool):
        self.student_id = student_id
        self.date = date
        self.present = present

# ========= Attendance Page (Interactive Panel) =========
class AttendancePage(tk.Frame):
    """Attendance tracking screen"""
    def __init__(self, root, back_callback):
        super().__init__(root, bg="#f5f5f5")
        self.root = root
        self.back_callback = back_callback

        # Sample students (could come from your app's data later)
        self.students = [
            Student(1, "Jordan Rashid"),
            Student(2, "Ivon Diaz"),
            Student(3, "Hadi Khan"),
        ]
        self.next_student_id = 4  # Track next available ID

        # To track Present/Absent choices
        self.attVars: dict[int, tk.StringVar] = {}

        # Top Bar / Back Button
        top_bar = tk.Frame(self, bg="#f5f5f5")
        top_bar.pack(fill="x", pady=(10, 0))

        backButton = tk.Button(
            top_bar,
            text="← Back",
            font=("Arial", 12),
            relief="flat",
            bg="#f5f5f5",
            fg="#063563",
            cursor="hand2",
            command=self.on_back
        )
        backButton.pack(side="left", padx=10)

        # Page Title
        gradeLevel = "K-4"  # placeholder grade level

        pageTitle = tk.Label(
            self,
            text=f"Attendance - Grade {gradeLevel}",
            font=("Arial", 20, "bold"),
            bg="#063563",
            fg="white",
            pady=10
        )
        pageTitle.pack(fill="x", pady=(5, 0))

        # Date Display with Day-Month-Year format
        attFullDate = date.today()

        weekday_index = attFullDate.weekday()
        if weekday_index < 5:
            weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            attWeekday = weekday_names[weekday_index]
        else:
            attWeekday = "Weekend"

        # Format: Day-Month-Year (e.g., "12-December-2025")
        month_names = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        attMonth = month_names[attFullDate.month - 1]
        attDay = attFullDate.day
        attYear = attFullDate.year

        self.dateLabel = tk.Label(
            self,
            text=f"{attWeekday}, {attDay}-{attMonth}-{attYear}",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        self.dateLabel.pack(pady=(10, 0))

        # Header frame for enrollment count and Add Student button
        header_frame = tk.Frame(self, bg="#f5f5f5")
        header_frame.pack(fill="x", pady=(0, 10), padx=20)

        # Enrollment Count
        self.enrollmentLabel = tk.Label(
            header_frame,
            text=f"{len(self.students)} students enrolled",
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#7f8c8d"
        )
        self.enrollmentLabel.pack(side="left")

        # Add Student Button
        addStudentButton = tk.Button(
            header_frame,
            text="+ Add Student",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.add_student
        )
        addStudentButton.pack(side="right")

        # Scrollable area for student list
        canvas = tk.Canvas(self, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))

        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.list_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Render student list
        self.render_student_list()

        # Submit Button
        submitButton = tk.Button(
            self,
            text="Submit to District",
            bg="#1aaf78",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.submit_attendance
        )
        submitButton.pack(pady=20)

    def render_student_list(self):
        """Render the complete student list"""
        # Clear existing rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Clear attendance vars for removed students
        self.attVars.clear()
        
        # Create rows for all students
        for student in self.students:
            self._create_student_row(student)
        
        # Update enrollment count
        self.enrollmentLabel.config(text=f"{len(self.students)} students enrolled")

    def _create_student_row(self, student: Student):
        """Create a row with the student name, Present/Absent buttons, and Remove button."""
        frame = tk.Frame(self.list_frame, bg="white", relief="solid", bd=1)
        frame.pack(fill="x", pady=5, padx=10)

        # Student name
        nameLabel = tk.Label(
            frame,
            text=student.name,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        nameLabel.pack(side="left", padx=10, pady=5)

        # Remove button
        removeButton = tk.Button(
            frame,
            text="✕",
            font=("Arial", 10, "bold"),
            bg="#E74C3C",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
            command=lambda s=student: self.remove_student(s)
        )
        removeButton.pack(side="right", padx=5)

        # Attendance radio buttons
        var = tk.StringVar(value="Present")
        self.attVars[student.student_id] = var

        presentButton = tk.Radiobutton(
            frame,
            text="Present",
            variable=var,
            value="Present",
            bg="white",
            fg="#27AE60",
            font=("Arial", 10)
        )
        presentButton.pack(side="right", padx=5)

        absentButton = tk.Radiobutton(
            frame,
            text="Absent",
            variable=var,
            value="Absent",
            bg="white",
            fg="#E74C3C",
            font=("Arial", 10)
        )
        absentButton.pack(side="right", padx=5)

    def add_student(self):
        """Open dialog to add a new student"""
        AddStudentDialog(self.root, self.add_student_callback)
    
    def add_student_callback(self, student_name):
        """Callback to add student to the list"""
        if student_name:
            new_student = Student(self.next_student_id, student_name)
            self.students.append(new_student)
            self.next_student_id += 1
            self.render_student_list()
            messagebox.showinfo("Success", f"Student '{student_name}' added successfully!")
    
    def remove_student(self, student: Student):
        """Remove a student from the list"""
        result = messagebox.askyesno(
            "Remove Student",
            f"Are you sure you want to remove {student.name} from the attendance list?"
        )
        
        if result:
            self.students = [s for s in self.students if s.student_id != student.student_id]
            self.render_student_list()
            messagebox.showinfo("Success", f"Student '{student.name}' removed successfully!")

    # Callbacks

    def on_back(self):
        """Go back to the previous screen (dashboard)."""
        self.back_callback()

    def submit_attendance(self):
        """Collect attendance, create AttendanceRecord objects, and show a summary."""
        if len(self.students) == 0:
            messagebox.showwarning("No Students", "Please add students before submitting attendance.")
            return
        
        today = date.today()
        records: list[AttendanceRecord] = []

        for student in self.students:
            status = self.attVars[student.student_id].get()
            present_flag = (status == "Present")
            records.append(AttendanceRecord(student.student_id, today, present_flag))

        # Calculate summary
        total = len(records)
        present_count = sum(1 for r in records if r.present)
        absent_count = total - present_count
        percent_present = (present_count / total * 100) if total > 0 else 0

        summary = (
            f"Attendance recorded for {total} students.\n\n"
            f"Present: {present_count}\n"
            f"Absent: {absent_count}\n"
            f"Attendance rate: {percent_present:.1f}%"
        )

        messagebox.showinfo("Attendance Submitted", summary)

    # Screen control for main app

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

class AddStudentDialog:
    """Dialog for adding a new student"""
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Student")
        self.dialog.geometry("400x200")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text="Add New Student",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="x", padx=30)
        
        tk.Label(
            form_frame,
            text="Student Name:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.name_entry.pack(fill="x", ipady=8)
        self.name_entry.focus()
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        add_btn = tk.Button(
            button_frame,
            text="Add Student",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.add_student
        )
        add_btn.pack(side="right")
        
        # Bind Enter key to add student
        self.name_entry.bind("<Return>", lambda e: self.add_student())
    
    def add_student(self):
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Validation Error", "Please enter a student name.")
            return
        
        self.callback(name)
        self.dialog.destroy()

# ========= Template & Lesson Dialogs (for Lesson Planning) =========
class TemplateDialog:
    """Dialog for creating or editing a lesson template"""
    def __init__(self, parent, callback, template_data=None):
        self.callback = callback
        self.template_data = template_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Template" if template_data else "Create New Template")
        self.dialog.geometry("500x600")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text="Edit Template" if template_data else "Create New Template",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Template Name
        tk.Label(
            form_frame,
            text="Template Name *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.name_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            self.name_entry.insert(0, template_data.get("name", ""))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(
            form_frame,
            textvariable=self.subject_var,
            font=("Arial", 11),
            state="readonly",
            values=["Reading", "Math", "Science", "Social Studies", "Art", "Physical Education", "Other"]
        )
        subject_combo.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            subject_combo.set(template_data.get("subject", "Select a subject"))
        else:
            subject_combo.set("Select a subject")
        
        # Duration
        tk.Label(
            form_frame,
            text="Duration (minutes) *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.duration_var = tk.StringVar()
        duration_combo = ttk.Combobox(
            form_frame,
            textvariable=self.duration_var,
            font=("Arial", 11),
            state="readonly",
            values=["15", "30", "45", "60", "90"]
        )
        duration_combo.pack(fill="x", ipady=8, pady=(0, 15))
        if template_data:
            duration_combo.set(template_data.get("duration", "45"))
        else:
            duration_combo.set("45")
        
        # Standards
        tk.Label(
            form_frame,
            text="Standards/Objectives",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.standards_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=3,
            wrap="word"
        )
        self.standards_text.pack(fill="x", pady=(0, 15))
        if template_data:
            self.standards_text.insert("1.0", template_data.get("standards", ""))
        
        # Activities/Materials
        tk.Label(
            form_frame,
            text="Activities/Materials",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.activities_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=4,
            wrap="word"
        )
        self.activities_text.pack(fill="x", pady=(0, 20))
        if template_data:
            self.activities_text.insert("1.0", template_data.get("activities", ""))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Save Template",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.save_template
        )
        save_btn.pack(side="right")
        
    def save_template(self):
        name = self.name_entry.get().strip()
        subject = self.subject_var.get()
        duration = self.duration_var.get()
        
        if not name:
            messagebox.showwarning("Validation Error", "Please enter a template name.")
            return
        
        if subject == "Select a subject":
            messagebox.showwarning("Validation Error", "Please select a subject.")
            return
        
        template_data = {
            "name": name,
            "subject": subject,
            "duration": duration,
            "standards": self.standards_text.get("1.0", "end-1c").strip(),
            "activities": self.activities_text.get("1.0", "end-1c").strip()
        }
        
        # If editing, preserve the original ID
        if self.template_data and "id" in self.template_data:
            template_data["id"] = self.template_data["id"]
        
        self.callback(template_data)
        self.dialog.destroy()

class LessonDialog:
    """Dialog for adding a new lesson"""
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Lesson")
        self.dialog.geometry("500x550")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"500x550+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text="Create New Lesson",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Lesson Title
        tk.Label(
            form_frame,
            text="Lesson Title *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.title_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.title_entry.pack(fill="x", ipady=8, pady=(0, 15))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(
            form_frame,
            textvariable=self.subject_var,
            font=("Arial", 11),
            state="readonly",
            values=["Reading", "Math", "Science", "Social Studies", "Art", "Physical Education", "Other"]
        )
        subject_combo.pack(fill="x", ipady=8, pady=(0, 15))
        subject_combo.set("Select a subject")
        
        # Standards
        tk.Label(
            form_frame,
            text="Standards/Objectives",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.standards_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=3,
            wrap="word"
        )
        self.standards_text.pack(fill="x", pady=(0, 15))
        
        # Duration
        tk.Label(
            form_frame,
            text="Duration (minutes)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.duration_var = tk.StringVar()
        duration_combo = ttk.Combobox(
            form_frame,
            textvariable=self.duration_var,
            font=("Arial", 11),
            state="readonly",
            values=["15", "30", "45", "60", "90"]
        )
        duration_combo.pack(fill="x", ipady=8, pady=(0, 15))
        duration_combo.set("45")
        
        # Notes
        tk.Label(
            form_frame,
            text="Notes",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.notes_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            height=4,
            wrap="word"
        )
        self.notes_text.pack(fill="x", pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left")
        
        save_btn = tk.Button(
            button_frame,
            text="Create Lesson",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.save_lesson
        )
        save_btn.pack(side="right")
        
    def save_lesson(self):
        title = self.title_entry.get().strip()
        subject = self.subject_var.get()
        
        if not title:
            messagebox.showwarning("Validation Error", "Please enter a lesson title.")
            return
        
        if subject == "Select a subject":
            messagebox.showwarning("Validation Error", "Please select a subject.")
            return
        
        lesson_data = {
            "title": title,
            "subject": subject,
            "standards": self.standards_text.get("1.0", "end-1c").strip(),
            "duration": self.duration_var.get(),
            "notes": self.notes_text.get("1.0", "end-1c").strip(),
            "progress": 0
        }
        
        self.callback(lesson_data)
        self.dialog.destroy()

# ========= Dashboard Screen =========
class DashboardScreen:
    """Main dashboard screen"""
    def __init__(
        self,
        root,
        switch_to_lessons_callback,
        switch_to_parent_comm_callback,
        switch_to_attendance_callback,
        switch_to_reports_callback,
        switch_to_iep_callback,
        switch_to_settings,
        switch_to_assessments,
        switch_to_ai
    ):
        self.root = root
        self.switch_to_lessons = switch_to_lessons_callback
        self.switch_to_parent_comm = switch_to_parent_comm_callback
        self.switch_to_attendance = switch_to_attendance_callback
        self.switch_to_reports = switch_to_reports_callback
        self.switch_to_iep = switch_to_iep_callback
        self.switch_to_settings = switch_to_settings
        self.switch_to_assessments = switch_to_assessments
        self.switch_to_ai = switch_to_ai
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_label = tk.Label(
            header,
            text="StreamlineEDU",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white",
            anchor="w"
        )
        header_label.pack(side="left", padx=30, pady=15)
        
        # User info
        user_frame = tk.Frame(header, bg="#2196F3")
        user_frame.pack(side="right", padx=30)
        
        user_circle = tk.Canvas(user_frame, width=40, height=40, bg="#2196F3", highlightthickness=0)
        user_circle.pack()
        user_circle.create_oval(2, 2, 38, 38, fill="#1976D2", outline="")
        user_circle.create_text(20, 20, text="IG", fill="white", font=("Arial", 12, "bold"))
        
        # Main content
        content = tk.Frame(self.frame, bg="#f5f5f5")
        content.pack(fill="both", expand=True, padx=40, pady=30)
        
        welcome_label = tk.Label(
            content,
            text="Welcome back!",
            font=("Arial", 24, "bold"),
            bg="#f5f5f5",
            fg="#212121"
        )
        welcome_label.pack(anchor="w", pady=(0, 5))
        
        tagline_label = tk.Label(
            content,
            text="Reclaim your time with intelligent classroom management",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#757575"
        )
        tagline_label.pack(anchor="w", pady=(0, 25))
        
        # Dashboard cards
        cards_container = tk.Frame(content, bg="#f5f5f5")
        cards_container.pack(fill="both", expand=True)
        
        # 1. Attendance Tracking (clickable)
        self.create_card(
            cards_container, 
            "1. Attendance Tracking", 
            "Track and manage student attendance",
            "#4CAF50",
            0, 0,
            clickable=True,
            click_callback=self.switch_to_attendance
        )
        
        # Lesson Planning card (clickable)
        self.create_card(
            cards_container,
            "2. Lesson Planning",
            "Plan and organize lessons",
            "#2196F3",
            0, 1,
            clickable=True,
            click_callback=self.switch_to_lessons
        )
        
        # Parent Communication card (clickable)
        self.create_card(
            cards_container,
            "3. Parent Communication",
            "Messages and updates",
            "#9C27B0",
            0, 2,
            clickable=True,
            click_callback=self.switch_to_parent_comm
        )
        
        self.create_card(
            cards_container,
            "4. IEP Progress Reports",
            "Individual education plans",
            "#F44336",
            0, 3,
            clickable=True,
            click_callback=self.switch_to_iep
        )
        
        self.create_card(
            cards_container,
            "5. Assessment Documentation",
            "Manage student assessments",
            "#FF9800",
            1, 0,
            clickable=True,
            click_callback=self.switch_to_assessments
        )
        
        self.create_card(
            cards_container,
            "6. AI Intelligent Assistant",
            "Smart classroom assistant",
            "#00BCD4",
            1, 1,
            clickable=True,
            click_callback=self.switch_to_ai
        )
        
        # Reports & Compliance (clickable)
        self.create_card(
            cards_container,
            "7. Reports & Compliance",
            "Generate reports and track compliance",
            "#795548",
            1, 2,
            clickable=True,
            click_callback=self.switch_to_reports
        )
        
        self.create_card(
            cards_container,
            "8. Settings & Profile",
            "Manage your account",
            "#607D8B",
            1, 3,
            clickable=True,
            click_callback=self.switch_to_settings
        )
        
    def create_card(self, parent, title, description, color, row, col, clickable=False, click_callback=None):
        card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1,
            cursor="hand2" if clickable else ""
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        if clickable and click_callback:
            card.bind("<Button-1>", lambda e: click_callback())
            
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=8)
        color_bar.pack(fill="x")
        
        # Content
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            content_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 10))
        
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        desc_label.pack(fill="x")
        
        if clickable and click_callback:
            for widget in [card, content_frame, title_label, desc_label]:
                widget.bind("<Button-1>", lambda e: click_callback())
        
        return card
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

# ========= Lesson Planning Screen =========
class LessonPlanningScreen:
    """Lesson planning screen with tabs"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.current_tab = "this_week"
        self.template_id_counter = 3  # For generating unique IDs
        
        # Sample data for different weeks
        self.lessons_data = {
            "this_week": [
                {
                    "day": "Monday, November 10",
                    "lessons": [
                        {"title": "Reading Comprehension", "progress": 75},
                        {"title": "Math - Multiplication Tables", "progress": 100}
                    ]
                },
                {
                    "day": "Tuesday, November 11",
                    "lessons": [
                        {"title": "Science - Plant Life Cycle", "progress": 50}
                    ]
                }
            ],
            "next_week": [
                {
                    "day": "Monday, November 17",
                    "lessons": [
                        {"title": "Writing Workshop", "progress": 0}
                    ]
                }
            ],
            "templates": [
                {
                    "id": 0,
                    "name": "Standard Math Lesson",
                    "subject": "Math",
                    "duration": "45",
                    "standards": "Common Core Math Standards",
                    "activities": "Warm-up exercises, direct instruction, guided practice, independent work"
                },
                {
                    "id": 1,
                    "name": "Reading Comprehension",
                    "subject": "Reading",
                    "duration": "60",
                    "standards": "Reading comprehension and analysis",
                    "activities": "Read aloud, group discussion, comprehension questions, writing response"
                },
                {
                    "id": 2,
                    "name": "Science Experiment",
                    "subject": "Science",
                    "duration": "90",
                    "standards": "Scientific method and inquiry",
                    "activities": "Hypothesis, materials setup, experiment, observation, conclusion"
                }
            ]
        }
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # StreamlineEDU branding
        branding_frame = tk.Frame(header, bg="#2196F3")
        branding_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white"
        ).pack(anchor="w")
        
        header_label = tk.Label(
            branding_frame,
            text="Lesson Planning",
            font=("Arial", 11),
            bg="#2196F3",
            fg="#E3F2FD",
            anchor="w"
        )
        header_label.pack(anchor="w")
        
        # Navigation bar
        nav_frame = tk.Frame(self.frame, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Label(
            nav_frame,
            text="← Back to Dashboard",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=20, pady=10)
        back_btn.bind("<Button-1>", lambda e: self.back_callback())
        
        # User initials
        user_circle = tk.Canvas(nav_frame, width=35, height=35, bg="#37474F", highlightthickness=0)
        user_circle.pack(side="right", padx=20)
        user_circle.create_oval(2, 2, 33, 33, fill="#78909C", outline="")
        user_circle.create_text(17.5, 17.5, text="IG", fill="white", font=("Arial", 10, "bold"))
        
        # Tab bar
        self.tab_frame = tk.Frame(self.frame, bg="white")
        self.tab_frame.pack(fill="x", pady=(0, 10))
        
        tab_container = tk.Frame(self.tab_frame, bg="white")
        tab_container.pack(anchor="w", padx=20, pady=10)
        
        # Tab buttons
        self.this_week_tab = tk.Label(
            tab_container,
            text="This Week",
            font=("Arial", 11),
            bg="white",
            fg="#2196F3",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.this_week_tab.pack(side="left", padx=(0, 20))
        self.this_week_tab.bind("<Button-1>", lambda e: self.switch_tab("this_week"))
        
        self.next_week_tab = tk.Label(
            tab_container,
            text="Next Week",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.next_week_tab.pack(side="left", padx=(0, 20))
        self.next_week_tab.bind("<Button-1>", lambda e: self.switch_tab("next_week"))
        
        self.templates_tab = tk.Label(
            tab_container,
            text="Templates",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.templates_tab.pack(side="left")
        self.templates_tab.bind("<Button-1>", lambda e: self.switch_tab("templates"))
        
        # Underline for active tab
        self.underline = tk.Frame(tab_container, bg="#2196F3", height=3, width=80)
        self.underline.place(x=10, y=30)
        
        # Scrollable content area
        self.content_canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.content_canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.content_canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        )
        
        self.content_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.content_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.content_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        self.content_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Render initial content
        self.render_content()
        
    def _on_mousewheel(self, event):
        self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        
        # Update tab colors
        self.this_week_tab.config(fg="#2196F3" if tab_name == "this_week" else "#757575")
        self.next_week_tab.config(fg="#2196F3" if tab_name == "next_week" else "#757575")
        self.templates_tab.config(fg="#2196F3" if tab_name == "templates" else "#757575")
        
        # Update underline position
        positions = {
            "this_week": 10,
            "next_week": 110,
            "templates": 230
        }
        self.underline.place(x=positions[tab_name], y=30)
        
        # Re-render content
        self.render_content()
        
    def render_content(self):
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if self.current_tab == "templates":
            self.render_templates()
        else:
            days_data = self.lessons_data[self.current_tab]
            for day_data in days_data:
                self.create_day_card(self.scrollable_frame, day_data)
            
            # Info banner
            self.create_info_banner(self.scrollable_frame)
    
    def render_templates(self):
        # Templates view header with create button
        header_frame = tk.Frame(self.scrollable_frame, bg="white")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header = tk.Label(
            header_frame,
            text="Lesson Templates",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        header.pack(side="left")
        
        create_btn = tk.Button(
            header_frame,
            text="+ Create Template",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.create_template
        )
        create_btn.pack(side="right")
        
        # Display templates
        templates = self.lessons_data["templates"]
        
        if not templates:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="No templates yet. Click 'Create Template' to add one.",
                font=("Arial", 11),
                bg="white",
                fg="#757575",
                anchor="w"
            )
            empty_label.pack(fill="x", padx=20, pady=20)
        else:
            for template in templates:
                self.create_template_card(self.scrollable_frame, template)
    
    def create_template_card(self, parent, template):
        template_card = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        template_card.pack(fill="x", padx=20, pady=5)
        
        # Main content area
        content_frame = tk.Frame(template_card, bg="white")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Left side - Template info
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Template name and subject
        name_label = tk.Label(
            info_frame,
            text=template["name"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        name_label.pack(fill="x")
        
        details_label = tk.Label(
            info_frame,
            text=f"{template['subject']} • {template['duration']} min",
            font=("Arial", 10),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        details_label.pack(fill="x", pady=(3, 0))
        
        # Right side - Action buttons
        button_frame = tk.Frame(content_frame, bg="white")
        button_frame.pack(side="right")
        
        edit_btn = tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=lambda: self.edit_template(template)
        )
        edit_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 9),
            bg="#F44336",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=lambda: self.delete_template(template)
        )
        delete_btn.pack(side="left")
    
    def create_template(self):
        def save_template_callback(template_data):
            # Assign a new ID
            template_data["id"] = self.template_id_counter
            self.template_id_counter += 1
            
            # Add template to the list
            self.lessons_data["templates"].append(template_data)
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template created successfully!")
        
        TemplateDialog(self.root, save_template_callback)
    
    def edit_template(self, template):
        def update_template_callback(updated_data):
            # Find and update the template
            for i, t in enumerate(self.lessons_data["templates"]):
                if t["id"] == template["id"]:
                    self.lessons_data["templates"][i] = updated_data
                    break
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template updated successfully!")
        
        TemplateDialog(self.root, update_template_callback, template)
    
    def delete_template(self, template):
        result = messagebox.askyesno(
            "Delete Template",
            f"Are you sure you want to delete the template '{template['name']}'?"
        )
        
        if result:
            # Remove the template
            self.lessons_data["templates"] = [
                t for t in self.lessons_data["templates"] if t["id"] != template["id"]
            ]
            
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Template deleted successfully!")
    
    def create_day_card(self, parent, day_data):
        card_frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 10), padx=20)
        
        # Card header
        card_header = tk.Frame(card_frame, bg="white")
        card_header.pack(fill="x", padx=20, pady=(15, 10))
        
        day_label = tk.Label(
            card_header,
            text=day_data["day"],
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        )
        day_label.pack(side="left")
        
        add_btn = tk.Button(
            card_header,
            text="+ Add Lesson",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=lambda: self.add_lesson(day_data)
        )
        add_btn.pack(side="right")
        
        # Lessons
        for lesson in day_data["lessons"]:
            self.create_lesson_item(card_frame, lesson)
    
    def create_lesson_item(self, parent, lesson):
        lesson_frame = tk.Frame(parent, bg="white")
        lesson_frame.pack(fill="x", padx=20, pady=10)
        
        # Blue vertical line
        line = tk.Frame(lesson_frame, bg="#2196F3", width=4)
        line.pack(side="left", fill="y", padx=(0, 15))
        
        lesson_content = tk.Frame(lesson_frame, bg="white")
        lesson_content.pack(side="left", fill="x", expand=True)
        
        lesson_title = tk.Label(
            lesson_content,
            text=lesson["title"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        lesson_title.pack(fill="x")
        
        # Progress bar
        progress_bg = tk.Canvas(lesson_content, height=8, bg="white", highlightthickness=0)
        progress_bg.pack(fill="x", pady=(8, 3))
        
        max_width = 400
        progress_width = int((lesson["progress"] / 100) * max_width)
        
        progress_bg.create_rectangle(0, 0, max_width, 8, fill="#E0E0E0", outline="")
        progress_bg.create_rectangle(0, 0, progress_width, 8, fill="#4CAF50", outline="")
        
        # Status label
        if lesson["progress"] == 100:
            status_text = "Complete ✓"
            status_color = "#4CAF50"
        else:
            status_text = f"{lesson['progress']}% complete"
            status_color = "#757575"
        
        status_label = tk.Label(
            lesson_content,
            text=status_text,
            font=("Arial", 9),
            bg="white",
            fg=status_color,
            anchor="w"
        )
        status_label.pack(fill="x")
    
    def create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFF9C4", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", pady=10, padx=20)
        
        # Yellow vertical line
        yellow_line = tk.Frame(info_frame, bg="#FFC107", width=5)
        yellow_line.pack(side="left", fill="y")
        
        info_content = tk.Frame(info_frame, bg="#FFF9C4")
        info_content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
        
        info_title = tk.Label(
            info_content,
            text="Auto-populated with standards:",
            font=("Arial", 10, "bold"),
            bg="#FFF9C4",
            fg="#212121",
            anchor="w"
        )
        info_title.pack(fill="x")
        
        info_text = tk.Label(
            info_content,
            text="System suggests aligned resources and activities based on curriculum.",
            font=("Arial", 10),
            bg="#FFF9C4",
            fg="#212121",
            anchor="w"
        )
        info_text.pack(fill="x")
    
    def add_lesson(self, day_data):
        def save_lesson_callback(lesson_data):
            # Add new lesson to the day
            day_data["lessons"].append({
                "title": f"{lesson_data['subject']} - {lesson_data['title']}",
                "progress": 0
            })
            # Re-render the content
            self.render_content()
            messagebox.showinfo("Success", "Lesson created successfully!")
        
        LessonDialog(self.root, save_lesson_callback)
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

# ========= Parent Communication & Message Dialogs =========
class MessageComposerDialog:
    """Dialog for composing or editing email messages"""
    def __init__(self, parent, callback, draft_data=None, mode="new"):
        self.callback = callback
        self.draft_data = draft_data
        self.mode = mode  # "new", "edit", or "review"
        self.dialog = tk.Toplevel(parent)
        
        title_map = {
            "new": "New Message",
            "edit": "Edit Draft",
            "review": "Review & Send Message"
        }
        self.dialog.title(title_map.get(mode, "Message Composer"))
        self.dialog.geometry("600x700")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
        
        # Header
        header_text = title_map.get(mode, "Message Composer")
        if mode == "review":
            header_text = "Review AI-Generated Message"
        
        header = tk.Label(
            self.dialog,
            text=header_text,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # AI Badge for review mode
        if mode == "review":
            ai_badge = tk.Label(
                self.dialog,
                text="✨ AI Generated - Please review before sending",
                font=("Arial", 10),
                bg="#E3F2FD",
                fg="#2196F3",
                padx=15,
                pady=8
            )
            ai_badge.pack(pady=(0, 15))
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # To (Recipient)
        tk.Label(
            form_frame,
            text="To: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.to_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.to_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if draft_data:
            self.to_entry.insert(0, draft_data.get("recipient", ""))
        
        # Subject
        tk.Label(
            form_frame,
            text="Subject: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.subject_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.subject_entry.pack(fill="x", ipady=8, pady=(0, 15))
        if draft_data:
            self.subject_entry.insert(0, draft_data.get("subject", ""))
        
        # Message Body
        tk.Label(
            form_frame,
            text="Message: *",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Text widget with scrollbar
        text_container = tk.Frame(form_frame, relief="solid", borderwidth=1)
        text_container.pack(fill="both", expand=True, pady=(0, 15))
        
        text_scrollbar = tk.Scrollbar(text_container)
        text_scrollbar.pack(side="right", fill="y")
        
        self.message_text = tk.Text(
            text_container,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=text_scrollbar.set
        )
        self.message_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        text_scrollbar.config(command=self.message_text.yview)
        
        if draft_data:
            # For review/edit mode, use the full preview text or generate a complete message
            if mode == "review":
                body = draft_data.get("preview", "") + "\n\nBest regards,\nYour Name\n\n---\nSent via StreamlineEDU"
            else:
                body = draft_data.get("body", draft_data.get("preview", ""))
            self.message_text.insert("1.0", body)
        
        # Priority checkbox
        self.priority_var = tk.BooleanVar()
        priority_check = tk.Checkbutton(
            form_frame,
            text="Mark as high priority",
            variable=self.priority_var,
            font=("Arial", 10),
            bg="white",
            fg="#212121"
        )
        priority_check.pack(anchor="w", pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Different button layouts based on mode
        if mode == "review":
            # Review mode: Edit Draft, Discard, Send
            discard_btn = tk.Button(
                button_frame,
                text="Discard",
                font=("Arial", 11),
                bg="#F44336",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.discard_draft
            )
            discard_btn.pack(side="left")
            
            edit_draft_btn = tk.Button(
                button_frame,
                text="Edit Draft",
                font=("Arial", 11),
                bg="#9E9E9E",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.switch_to_edit
            )
            edit_draft_btn.pack(side="left", padx=(10, 0))
            
            send_btn = tk.Button(
                button_frame,
                text="Send Message",
                font=("Arial", 11, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                command=self.send_message
            )
            send_btn.pack(side="right")
        else:
            # New/Edit mode: Cancel, Save Draft, Send
            cancel_btn = tk.Button(
                button_frame,
                text="Cancel",
                font=("Arial", 11),
                bg="#E0E0E0",
                fg="#212121",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                command=self.dialog.destroy
            )
            cancel_btn.pack(side="left")
            
            save_draft_btn = tk.Button(
                button_frame,
                text="Save Draft",
                font=("Arial", 11),
                bg="#9E9E9E",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8,
                command=self.save_draft
            )
            save_draft_btn.pack(side="left", padx=(10, 0))
            
            send_btn = tk.Button(
                button_frame,
                text="Send",
                font=("Arial", 11, "bold"),
                bg="#4CAF50",
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                command=self.send_message
            )
            send_btn.pack(side="right")
    
    def send_message(self):
        recipient = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.message_text.get("1.0", "end-1c").strip()
        
        if not recipient:
            messagebox.showwarning("Validation Error", "Please enter a recipient.")
            return
        
        if not subject:
            messagebox.showwarning("Validation Error", "Please enter a subject.")
            return
        
        if not body:
            messagebox.showwarning("Validation Error", "Please enter a message.")
            return
        
        message_data = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "priority": self.priority_var.get(),
            "status": "sent",
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        
        self.callback(message_data, "send")
        self.dialog.destroy()
        messagebox.showinfo("Success", f"Message sent to {recipient}!")
    
    def save_draft(self):
        recipient = self.to_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.message_text.get("1.0", "end-1c").strip()
        
        if not recipient and not subject and not body:
            messagebox.showwarning("Empty Draft", "Cannot save an empty draft.")
            return
        
        message_data = {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "preview": body[:100] + "..." if len(body) > 100 else body,
            "priority": self.priority_var.get(),
            "status": "draft",
            "generated_time": "Just now"
        }
        
        self.callback(message_data, "save_draft")
        self.dialog.destroy()
        messagebox.showinfo("Saved", "Draft saved successfully!")
    
    def discard_draft(self):
        result = messagebox.askyesno(
            "Discard Draft",
            "Are you sure you want to discard this draft?"
        )
        if result:
            if self.draft_data:
                self.callback(self.draft_data, "discard")
            self.dialog.destroy()
    
    def switch_to_edit(self):
        """Switch from review mode to edit mode"""
        self.dialog.destroy()
        # Re-open in edit mode handled by parent

class ParentCommunicationScreen:
    """Parent communication screen with messaging features"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.message_id_counter = 3  # For generating unique message IDs
        
        # Sample data for messages
        self.messages_data = {
            "drafts": [
                {
                    "id": 0,
                    "subject": "Re: Emma's Progress",
                    "preview": "Dear Mrs. Anderson, Emma has shown excellent progress in reading comprehension this week...",
                    "body": "Dear Mrs. Anderson,\n\nEmma has shown excellent progress in reading comprehension this week. She has been actively participating in group discussions and her test scores have improved significantly.\n\nShe particularly excelled in identifying main ideas and supporting details in the stories we've been reading. I'm very pleased with her dedication and effort.\n\nPlease let me know if you have any questions or would like to schedule a meeting to discuss her progress further.",
                    "recipient": "Mrs. Anderson",
                    "generated_time": "2 hrs ago",
                    "status": "draft"
                }
            ],
            "recent": [
                {
                    "id": 1,
                    "sender": "Mrs. Chen",
                    "subject": "Re: James homework assignment",
                    "time": "10:30 AM",
                    "unread": True
                },
                {
                    "id": 2,
                    "sender": "Mr. Garcia",
                    "subject": "Question about field trip permission",
                    "time": "Yesterday",
                    "unread": False
                }
            ]
        }
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#9C27B0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # StreamlineEDU branding
        branding_frame = tk.Frame(header, bg="#9C27B0")
        branding_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#9C27B0",
            fg="white"
        ).pack(anchor="w")
        
        header_label = tk.Label(
            branding_frame,
            text="Parent Communication",
            font=("Arial", 11),
            bg="#9C27B0",
            fg="#F3E5F5",
            anchor="w"
        )
        header_label.pack(anchor="w")
        
        # Navigation bar
        nav_frame = tk.Frame(self.frame, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Label(
            nav_frame,
            text="← Back  Messages",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=20, pady=10)
        back_btn.bind("<Button-1>", lambda e: self.back_callback())
        
        # User initials
        user_circle = tk.Canvas(nav_frame, width=35, height=35, bg="#37474F", highlightthickness=0)
        user_circle.pack(side="right", padx=20)
        user_circle.create_oval(2, 2, 33, 33, fill="#78909C", outline="")
        user_circle.create_text(17.5, 17.5, text="IG", fill="white", font=("Arial", 10, "bold"))
        
        # Main content area
        content_frame = tk.Frame(self.frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Inbox header with New Message button
        inbox_header = tk.Frame(content_frame, bg="white")
        inbox_header.pack(fill="x", pady=(0, 10))
        
        inbox_info = tk.Frame(inbox_header, bg="white")
        inbox_info.pack(side="left")
        
        inbox_label = tk.Label(
            inbox_info,
            text="Inbox",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        )
        inbox_label.pack(anchor="w")
        
        needs_attention = tk.Label(
            inbox_info,
            text="5 messages need attention",
            font=("Arial", 10),
            bg="white",
            fg="#757575",
            anchor="w"
        )
        needs_attention.pack(anchor="w")
        
        new_msg_btn = tk.Button(
            inbox_header,
            text="+ New Message",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.create_new_message
        )
        new_msg_btn.pack(side="right")
        
        # Scrollable content
        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # AI Drafts section
        self.scrollable_frame = scrollable_frame
        self.create_ai_drafts_section(scrollable_frame)
        
        # Recent Messages section
        self.create_recent_messages_section(scrollable_frame)
        
        # Info banner
        self.create_info_banner(scrollable_frame)
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_ai_drafts_section(self, parent):
        drafts_container = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        drafts_container.pack(fill="x", pady=(0, 15))
        
        # Header
        drafts_header = tk.Frame(drafts_container, bg="white")
        drafts_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(
            drafts_header,
            text="Drafts Generated by AI",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")
        
        tk.Label(
            drafts_header,
            text="AI Assisted",
            font=("Arial", 9),
            bg="#E3F2FD",
            fg="#2196F3",
            padx=8,
            pady=2
        ).pack(side="right")
        
        # Draft messages or empty state
        if not self.messages_data["drafts"]:
            empty_label = tk.Label(
                drafts_container,
                text="No drafts available. AI will generate helpful draft responses as needed.",
                font=("Arial", 10),
                bg="white",
                fg="#757575",
                anchor="w"
            )
            empty_label.pack(fill="x", padx=20, pady=(0, 15))
        else:
            for draft in self.messages_data["drafts"]:
                self.create_draft_item(drafts_container, draft)
    
    def create_draft_item(self, parent, draft):
        draft_frame = tk.Frame(parent, bg="#F5F5F5")
        draft_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Subject and time
        subject_frame = tk.Frame(draft_frame, bg="#F5F5F5")
        subject_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        tk.Label(
            subject_frame,
            text=draft["subject"],
            font=("Arial", 11, "bold"),
            bg="#F5F5F5",
            fg="#212121"
        ).pack(side="left")
        
        tk.Label(
            subject_frame,
            text=f"Generated {draft['generated_time']}",
            font=("Arial", 9),
            bg="#F5F5F5",
            fg="#757575"
        ).pack(side="right")
        
        # Preview text
        preview_label = tk.Label(
            draft_frame,
            text=draft["preview"],
            font=("Arial", 10),
            bg="#F5F5F5",
            fg="#424242",
            anchor="w",
            justify="left",
            wraplength=450
        )
        preview_label.pack(fill="x", padx=15, pady=(0, 10))
        
        # Action buttons
        button_frame = tk.Frame(draft_frame, bg="#F5F5F5")
        button_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        review_btn = tk.Button(
            button_frame,
            text="Review & Send",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=lambda: self.review_draft(draft)
        )
        review_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = tk.Button(
            button_frame,
            text="Edit",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=lambda: self.edit_draft(draft)
        )
        edit_btn.pack(side="left")
    
    def create_recent_messages_section(self, parent):
        recent_container = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        recent_container.pack(fill="x", pady=(0, 15))
        
        # Header
        tk.Label(
            recent_container,
            text="Recent Messages",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 10))
        
        # Recent messages
        for message in self.messages_data["recent"]:
            self.create_message_item(recent_container, message)
    
    def create_message_item(self, parent, message):
        message_frame = tk.Frame(
            parent, 
            bg="white",
            cursor="hand2"
        )
        message_frame.pack(fill="x", padx=20, pady=5)
        message_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Blue indicator line for unread
        if message.get("unread", False):
            indicator = tk.Frame(message_frame, bg="#2196F3", width=4)
            indicator.pack(side="left", fill="y", padx=(0, 10))
        else:
            # Spacer for alignment
            spacer = tk.Frame(message_frame, bg="white", width=4)
            spacer.pack(side="left", padx=(0, 10))
        
        # Message content
        content_frame = tk.Frame(message_frame, bg="white")
        content_frame.pack(side="left", fill="x", expand=True)
        content_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Sender and time
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x")
        header_frame.bind("<Button-1>", lambda e: self.open_message(message))
        
        sender_label = tk.Label(
            header_frame,
            text=message["sender"],
            font=("Arial", 11, "bold" if message.get("unread", False) else "normal"),
            bg="white",
            fg="#212121"
        )
        sender_label.pack(side="left")
        sender_label.bind("<Button-1>", lambda e: self.open_message(message))
        
        time_label = tk.Label(
            header_frame,
            text=message["time"],
            font=("Arial", 9),
            bg="white",
            fg="#757575"
        )
        time_label.pack(side="right")
        time_label.bind("<Button-1>", lambda e: self.open_message(message))
        
        # Subject
        subject_label = tk.Label(
            content_frame,
            text=message["subject"],
            font=("Arial", 10),
            bg="white",
            fg="#616161",
            anchor="w"
        )
        subject_label.pack(fill="x", pady=(2, 8))
        subject_label.bind("<Button-1>", lambda e: self.open_message(message))
    
    def create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFFDE7", relief="solid", borderwidth=1)
        info_frame.pack(fill="x")
        
        # Yellow vertical line
        yellow_line = tk.Frame(info_frame, bg="#FBC02D", width=5)
        yellow_line.pack(side="left", fill="y")
        
        info_content = tk.Frame(info_frame, bg="#FFFDE7")
        info_content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
        
        info_title = tk.Label(
            info_content,
            text="60% inbox reduction:",
            font=("Arial", 10, "bold"),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w"
        )
        info_title.pack(fill="x")
        
        info_text = tk.Label(
            info_content,
            text="AI assistant handles common questions automatically, flagging only items needing personal attention.",
            font=("Arial", 10),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w",
            wraplength=450,
            justify="left"
        )
        info_text.pack(fill="x")
    
    def create_new_message(self):
        def message_callback(message_data, action):
            if action == "send":
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "save_draft":
                # Add to drafts
                message_data["id"] = self.message_id_counter
                self.messages_data["drafts"].append(message_data)
                self.message_id_counter += 1
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, mode="new")
    
    def review_draft(self, draft):
        def message_callback(message_data, action):
            if action == "send":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "discard":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, draft_data=draft, mode="review")
    
    def edit_draft(self, draft):
        def message_callback(message_data, action):
            if action == "send":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
                # Add to recent messages
                self.messages_data["recent"].insert(0, {
                    "id": self.message_id_counter,
                    "sender": "You",
                    "subject": f"To: {message_data['recipient']} - {message_data['subject']}",
                    "time": message_data["timestamp"],
                    "unread": False
                })
                self.message_id_counter += 1
            elif action == "save_draft":
                # Update the draft
                for i, d in enumerate(self.messages_data["drafts"]):
                    if d["id"] == draft["id"]:
                        message_data["id"] = draft["id"]
                        self.messages_data["drafts"][i] = message_data
                        break
            elif action == "discard":
                # Remove from drafts
                self.messages_data["drafts"] = [
                    d for d in self.messages_data["drafts"] if d["id"] != draft["id"]
                ]
            
            # Refresh the display
            self.refresh_content()
        
        MessageComposerDialog(self.root, message_callback, draft_data=draft, mode="edit")
    
    def refresh_content(self):
        """Refresh the scrollable content area"""
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recreate sections
        self.create_ai_drafts_section(self.scrollable_frame)
        self.create_recent_messages_section(self.scrollable_frame)
        self.create_info_banner(self.scrollable_frame)
    
    def open_message(self, message):
        # Mark as read
        message["unread"] = False
        messagebox.showinfo("Message", f"From: {message['sender']}\n\n{message['subject']}")
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

# ========= IEP Progress Reports Screen =========
class IEPProgressReportsScreen:
    """IEP Progress Reports screen with student tracking"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        
        # Sample data for IEP students
        self.students_data = [
            {
                "id": 0,
                "name": "Marcus Johnson",
                "review_due": "November 15, 2025",
                "goals": [
                    {
                        "category": "Reading Goals",
                        "description": "Marcus has made substantial progress on his reading fluency goal. Current reading level has improved from 2.1 to 2.5 grade equivalent. He consistently participates in small group reading activities.",
                        "progress": 70
                    },
                    {
                        "category": "Math Goals",
                        "description": "Demonstrates understanding of basic addition and subtraction. Requires continued support with word problems and multi-step calculations.",
                        "progress": 55
                    }
                ]
            },
            {
                "id": 1,
                "name": "Sarah Williams",
                "review_due": "December 1, 2025",
                "goals": [
                    {
                        "category": "Communication Goals",
                        "description": "Shows improved verbal expression in structured settings. Continues to work on initiating conversations with peers.",
                        "progress": 65
                    }
                ]
            },
            {
                "id": 2,
                "name": "David Chen",
                "review_due": "November 20, 2025",
                "goals": [
                    {
                        "category": "Behavioral Goals",
                        "description": "Significant improvement in self-regulation strategies. Successfully uses calm-down techniques 80% of the time.",
                        "progress": 80
                    }
                ]
            }
        ]
        
        self.current_student = self.students_data[0]  # Default to first student
        
        self.frame = tk.Frame(root, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.frame, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # StreamlineEDU branding
        branding_frame = tk.Frame(header, bg="#2196F3")
        branding_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white"
        ).pack(anchor="w")
        
        header_label = tk.Label(
            branding_frame,
            text="IEP Progress Reports",
            font=("Arial", 11),
            bg="#2196F3",
            fg="#E3F2FD",
            anchor="w"
        )
        header_label.pack(anchor="w")
        
        # Navigation bar
        nav_frame = tk.Frame(self.frame, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)
        
        back_btn = tk.Label(
            nav_frame,
            text="← Back  IEP Progress",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=20, pady=10)
        back_btn.bind("<Button-1>", lambda e: self.back_callback())
        
        # User initials
        user_circle = tk.Canvas(nav_frame, width=35, height=35, bg="#37474F", highlightthickness=0)
        user_circle.pack(side="right", padx=20)
        user_circle.create_oval(2, 2, 33, 33, fill="#78909C", outline="")
        user_circle.create_text(17.5, 17.5, text="IG", fill="white", font=("Arial", 10, "bold"))
        
        # Main content area
        content_frame = tk.Frame(self.frame, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Student selector
        selector_frame = tk.Frame(content_frame, bg="white")
        selector_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            selector_frame,
            text="Select Student:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left", padx=(0, 10))
        
        self.student_var = tk.StringVar()
        student_names = [s["name"] for s in self.students_data]
        student_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.student_var,
            font=("Arial", 11),
            state="readonly",
            values=student_names,
            width=30
        )
        student_combo.pack(side="left")
        student_combo.set(self.current_student["name"])
        student_combo.bind("<<ComboboxSelected>>", self.on_student_selected)
        
        # Scrollable content
        canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Render student content
        self.render_student_content()
    
    def on_student_selected(self, event):
        selected_name = self.student_var.get()
        for student in self.students_data:
            if student["name"] == selected_name:
                self.current_student = student
                break
        self.render_student_content()
    
    def render_student_content(self):
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Student header
        student_header = tk.Frame(self.scrollable_frame, bg="white")
        student_header.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            student_header,
            text=f"Student: {self.current_student['name']}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        ).pack(anchor="w")
        
        tk.Label(
            student_header,
            text=f"IEP Review Due: {self.current_student['review_due']}",
            font=("Arial", 11),
            bg="white",
            fg="#757575"
        ).pack(anchor="w", pady=(3, 0))
        
        # Auto-Generated Progress Summary section
        self.create_progress_summary_section(self.scrollable_frame)
        
        # Action buttons
        self.create_action_buttons(self.scrollable_frame)
        
        # Info banner
        self.create_info_banner(self.scrollable_frame)
    
    def create_progress_summary_section(self, parent):
        summary_container = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        summary_container.pack(fill="x", pady=(15, 20))
        
        # Header
        summary_header = tk.Frame(summary_container, bg="white")
        summary_header.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(
            summary_header,
            text="Auto-Generated Progress Summary",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")
        
        tk.Label(
            summary_header,
            text="AI Generated",
            font=("Arial", 9),
            bg="#E3F2FD",
            fg="#2196F3",
            padx=8,
            pady=2
        ).pack(side="right")
        
        # Goals
        for goal in self.current_student["goals"]:
            self.create_goal_item(summary_container, goal)
    
    def create_goal_item(self, parent, goal):
        goal_frame = tk.Frame(parent, bg="white")
        goal_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Goal category
        tk.Label(
            goal_frame,
            text=goal["category"],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        # Goal description
        desc_label = tk.Label(
            goal_frame,
            text=goal["description"],
            font=("Arial", 10),
            bg="white",
            fg="#424242",
            anchor="w",
            justify="left",
            wraplength=700
        )
        desc_label.pack(fill="x", pady=(0, 8))
        
        # Progress bar
        progress_bg = tk.Canvas(goal_frame, height=10, bg="white", highlightthickness=0)
        progress_bg.pack(fill="x", pady=(0, 3))
        
        max_width = 700
        progress_width = int((goal["progress"] / 100) * max_width)
        
        progress_bg.create_rectangle(0, 0, max_width, 10, fill="#E0E0E0", outline="")
        progress_bg.create_rectangle(0, 0, progress_width, 10, fill="#4CAF50", outline="")
        
        # Progress percentage
        tk.Label(
            goal_frame,
            text=f"{goal['progress']}% of goal achieved",
            font=("Arial", 9),
            bg="white",
            fg="#757575",
            anchor="w"
        ).pack(fill="x")
    
    def create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="white")
        button_frame.pack(fill="x", pady=(10, 20))
        
        export_btn = tk.Button(
            button_frame,
            text="Export Report",
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.export_report
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        notes_btn = tk.Button(
            button_frame,
            text="Add Notes",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.add_notes
        )
        notes_btn.pack(side="left", padx=(0, 10))
        
        history_btn = tk.Button(
            button_frame,
            text="View History",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.view_history
        )
        history_btn.pack(side="left")
    
    def create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFFDE7", relief="solid", borderwidth=1)
        info_frame.pack(fill="x")
        
        # Yellow vertical line
        yellow_line = tk.Frame(info_frame, bg="#FBC02D", width=5)
        yellow_line.pack(side="left", fill="y")
        
        info_content = tk.Frame(info_frame, bg="#FFFDE7")
        info_content.pack(side="left", fill="x", expand=True, padx=15, pady=12)
        
        info_title = tk.Label(
            info_content,
            text="Automated data integration:",
            font=("Arial", 10, "bold"),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w"
        )
        info_title.pack(fill="x")
        
        info_text = tk.Label(
            info_content,
            text="Progress reports pull from classroom assessments, attendance, and behavioral data automatically.",
            font=("Arial", 10),
            bg="#FFFDE7",
            fg="#212121",
            anchor="w",
            wraplength=700,
            justify="left"
        )
        info_text.pack(fill="x")
    
    def export_report(self):
        messagebox.showinfo(
            "Export Report",
            f"Exporting IEP progress report for {self.current_student['name']}...\n\nReport will be saved as PDF."
        )
    
    def add_notes(self):
        NotesDialog(self.root, self.current_student)
    
    def view_history(self):
        messagebox.showinfo(
            "View History",
            f"Viewing historical IEP reports for {self.current_student['name']}..."
        )
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

# ========= Assessments =========
class AssesmentsPage(tk.Frame):
    """Uses same backbone as reports and compliance, but showcases assesments instead"""
    def __init__(self, root, back_callback=None):
        super().__init__(root, bg="#f5f5f5")
        self.root = root
        self.back_callback = back_callback

        # ================= STATE =================
        self.current_tab = "required"  # Recent | By Student | By Subject

        self.assessment_summary = {
            "title": "Reading Assessment - Week of Nov 3",
            "completed": 22,
            "proficient": 18,
            "developing": 3,
            "support": 1
        }

        self.recent_entries = [
            {
                "name": "Math Quiz - Multiplication",
                "date": "Nov 6, 2025",
                "students": 22,
                "detail": "Avg Score: 85%"
            },
            {
                "name": "Science Observation Notes",
                "date": "Nov 5, 2025",
                "students": 22,
                "detail": "Plant Growth Unit"
            }
        ]

        # ================= NAV BAR =================
        nav_frame = tk.Frame(self, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        back_label = tk.Label(
            nav_frame,
            text="← Back  Assessments",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_label.pack(side="left", padx=20)
        back_label.bind("<Button-1>", lambda e: self.on_back())

        user_canvas = tk.Canvas(
            nav_frame, width=35, height=35,
            bg="#37474F", highlightthickness=0
        )
        user_canvas.pack(side="right", padx=20)
        user_canvas.create_oval(2, 2, 33, 33, fill="#90A4AE", outline="")
        user_canvas.create_text(17.5, 17.5, text="IG",
                                fill="white", font=("Arial", 10, "bold"))

        # ================= TAB BAR =================
        tab_bar = tk.Frame(self, bg="white")
        tab_bar.pack(fill="x")

        tab_container = tk.Frame(tab_bar, bg="white")
        tab_container.pack(anchor="w", padx=20, pady=10)

        self.required_tab = tk.Label(
            tab_container, text="Recent",
            font=("Arial", 11),
            bg="white", fg="#1976D2",
            padx=10, pady=5, cursor="hand2"
        )
        self.required_tab.pack(side="left", padx=(0, 15))
        self.required_tab.bind("<Button-1>", lambda e: self.switch_tab("required"))

        self.custom_tab = tk.Label(
            tab_container, text="By Student",
            font=("Arial", 11),
            bg="white", fg="#757575",
            padx=10, pady=5, cursor="hand2"
        )
        self.custom_tab.pack(side="left", padx=(0, 15))
        self.custom_tab.bind("<Button-1>", lambda e: self.switch_tab("custom"))

        self.export_tab = tk.Label(
            tab_container, text="By Subject",
            font=("Arial", 11),
            bg="white", fg="#757575",
            padx=10, pady=5, cursor="hand2"
        )
        self.export_tab.pack(side="left")
        self.export_tab.bind("<Button-1>", lambda e: self.switch_tab("export"))

        self.underline = tk.Frame(tab_container, bg="#1976D2", height=3, width=90)
        self.underline.place(x=10, y=30)

        # ================= SCROLLABLE CONTENT =================
        content_outer = tk.Frame(self, bg="#f5f5f5")
        content_outer.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(content_outer, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(content_outer, orient="vertical",
                                 command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        self.render_content()

    # ================= TAB LOGIC =================

    def switch_tab(self, tab_name):
        self.current_tab = tab_name

        self.required_tab.config(
            fg="#1976D2" if tab_name == "required" else "#757575")
        self.custom_tab.config(
            fg="#1976D2" if tab_name == "custom" else "#757575")
        self.export_tab.config(
            fg="#1976D2" if tab_name == "export" else "#757575")

        positions = {"required": 10, "custom": 120, "export": 260}
        self.underline.place(x=positions[tab_name], y=30)

        self.render_content()

    def render_content(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if self.current_tab == "required":
            self._create_assessment_overview(self.scroll_frame)
            self._create_recent_entries(self.scroll_frame)
        else:
            self._create_placeholder(self.scroll_frame)

    # ================= SECTIONS =================

    def _create_assessment_overview(self, parent):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        card.pack(fill="x", pady=(0, 15))

        header = tk.Frame(card, bg="white")
        header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header, text=self.assessment_summary["title"],
            font=("Arial", 13, "bold"),
            bg="white", fg="#263238"
        ).pack(side="left")

        tk.Label(
            header,
            text=f'{self.assessment_summary["completed"]} students completed',
            font=("Arial", 10),
            bg="white", fg="#757575"
        ).pack(side="right")

        stats = tk.Frame(card, bg="white")
        stats.pack(fill="x", padx=20, pady=10)

        def stat_box(value, label, color):
            box = tk.Frame(stats, bg="#FAFAFA", relief="solid", bd=1)
            box.pack(side="left", expand=True, fill="x", padx=5)

            tk.Label(
                box, text=str(value),
                font=("Arial", 18, "bold"),
                fg=color, bg="#FAFAFA"
            ).pack(pady=(10, 0))

            tk.Label(
                box, text=label,
                font=("Arial", 10),
                fg="#757575", bg="#FAFAFA"
            ).pack(pady=(0, 10))

        stat_box(self.assessment_summary["proficient"], "Proficient", "#4CAF50")
        stat_box(self.assessment_summary["developing"], "Developing", "#F9A825")
        stat_box(self.assessment_summary["support"], "Needs Support", "#E53935")

        tk.Button(
            card,
            text="Generate Class Report",
            font=("Arial", 11, "bold"),
            bg="#5A9BD5",
            fg="white",
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.simulate_generate_assessment_report
        ).pack(fill="x", padx=20, pady=(10, 15))

    def _create_recent_entries(self, parent):
        container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        container.pack(fill="x")

        tk.Label(
            container, text="Recent Entries",
            font=("Arial", 13, "bold"),
            bg="white", fg="#263238"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        for entry in self.recent_entries:
            row = tk.Frame(container, bg="#FAFAFA")
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(
                row, text=entry["name"],
                font=("Arial", 11, "bold"),
                bg="#FAFAFA", fg="#37474F"
            ).pack(anchor="w")

            tk.Label(
                row,
                text=f'{entry["date"]} • {entry["students"]} students • {entry["detail"]}',
                font=("Arial", 10),
                bg="#FAFAFA", fg="#757575"
            ).pack(anchor="w", pady=(0, 8))

    def _create_placeholder(self, parent):
        tk.Label(
            parent,
            text="This view will be implemented next.",
            font=("Arial", 11),
            bg="#f5f5f5",
            fg="#757575"
        ).pack(pady=50)

    # ================= ACTIONS =================

    def simulate_generate_assessment_report(self):
        messagebox.showinfo(
            "Generate Report",
            "This would generate a class-wide assessment report."
        )

    def on_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            self.root.destroy()

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

class NotesDialog:
    """Dialog for adding notes to IEP reports"""
    def __init__(self, parent, student):
        self.student = student
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Notes")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg="white")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        # Header
        header = tk.Label(
            self.dialog,
            text=f"Add Notes - {student['name']}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#212121"
        )
        header.pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # Note Type
        tk.Label(
            form_frame,
            text="Note Type:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.note_type_var = tk.StringVar()
        note_type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.note_type_var,
            font=("Arial", 11),
            state="readonly",
            values=["Progress Update", "Behavioral Observation", "Goal Modification", "Parent Meeting", "Other"]
        )
        note_type_combo.pack(fill="x", ipady=8, pady=(0, 15))
        note_type_combo.set("Progress Update")
        
        # Date
        tk.Label(
            form_frame,
            text="Date:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.date_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.date_entry.pack(fill="x", ipady=8, pady=(0, 15))
        self.date_entry.insert(0, datetime.now().strftime("%B %d, %Y"))
        
        # Notes
        tk.Label(
            form_frame,
            text="Notes:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Text widget with scrollbar
        text_container = tk.Frame(form_frame, relief="solid", borderwidth=1)
        text_container.pack(fill="both", expand=True, pady=(0, 20))
        
        text_scrollbar = tk.Scrollbar(text_container)
        text_scrollbar.pack(side="right", fill="y")
        
        self.notes_text = tk.Text(
            text_container,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=text_scrollbar.set
        )
        self.notes_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        text_scrollbar.config(command=self.notes_text.yview)
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#212121",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = tk.Button(
            button_frame,
            text="Save Note",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.save_note
        )
        save_btn.pack(side="right")
    
    def save_note(self):
        note_type = self.note_type_var.get()
        date = self.date_entry.get().strip()
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        if not notes:
            messagebox.showwarning("Validation Error", "Please enter notes.")
            return
        
        self.dialog.destroy()
        messagebox.showinfo("Success", f"Note saved for {self.student['name']}!")

# ********* AI Assistant ********
class AIAssistantScreen:
    # AI features
    def showAiOutput(self, title, text):
        window = tk.Toplevel(self, root)
        window.title(title)
        window.geometry("600x400")
        window.configure(bg="white")

        windowlabel = tk.Label(window, text=title, font=("Arial", 14, "bold"), bg="white")
        windowlabel.pack(pady=(10,5))

        windowtxt = scrolledtext.ScrolledText(window, font=("Arial", 11), wrap="word", bg="#f9f9f9")
        windowtxt.pack(fill="both", expand=True, padx=20, pady=10)
        windowtxt.insert("1.0", text)
        windowtxt.config(state="disabled")

        windowbtn = tk.Button(window, text="Close", command=window.destroy, bg="#2196F3", fg="white", font=("Arial", 11, "bold"))
        windowbtn.pack(pady=10)

    def runGemini(self, prompt, title):
        try:
            response = client.models.generate_content( model="gemini-2.5-flash", contents = [prompt])
            text = response.text.strip()
        except Exception as e:
            text = f"Error: {e}"
            self.showAiOutput(title,text)
    def genParentUpdate(self):
        if client == "YOUR KEY HERE":
            messagebox.showwarning("API Key MISSING. You need to create your own Gemini API key to use the AI features here")
        else:
            prompt = ("Generate a professional, friendly, simple email draft written by a teacher explaining that if this app was fully running, pressing this button would generate a draft response that the teacher could send to a parent")
            self.runGemini(prompt, "Parent Update Draft")
            
    def genIepReport(self):
        if client == "YOUR KEY HERE":
           messagebox.showwarning("API Key MISSING. You need to create your own Gemini API key to use the AI features here")
        else:
            prompt = ("Generate a professional, friendly, simple draft explaining that no students needed an IEP")
            self.runGemini(prompt, "IEP Progress Report")

    def genLessonIdeas(self):
        if client == "YOUR KEY HERE":
                messagebox.showwarning("API Key MISSING. You need to create your own Gemini API key to use the AI features here")
        else:
                prompt = ("Generate a small list of ideas for a fun rainy 3rd grade classroomn day")
                self.runGemini(prompt, "Lesson Ideas")

    def genAnswers(self):
        if client == "YOUR KEY HERE":
            messagebox.showwarning("API Key MISSING. You need to create your own Gemini API key to use the AI features here")
        else:
            prompt = ("Generate answers to basic childrens questions, such as why is the sky blue or why do apples fall")
            self.runGemini(prompt, "Question Answers")

    def runGemini(self, prompt, title):
        try:
                response = client.models.generate_content( model="gemini-2.5-flash", contents = [prompt])
                text = response.text.strip()
        except Exception as e:
                text = f"Error: {e}"
                self.showAiOutput(title,text)
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="#f5f5f5")
        self.frame.configure(bg="#f5f5f5")

        # Header Section
        header = tk.Frame(self.frame, bg="#0078d4", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        back_button = tk.Label(
            header,
            text="← Back  AI Assistant",
            font=("Arial", 12),
            bg="#0078d4",
            fg="white",
            cursor="hand2"
        )
        back_button.pack(side="left", padx=20, pady=15)

        user_circle = Canvas(header, width=35, height=35, bg="#0078d4", highlightthickness=0)
        user_circle.pack(side="right", padx=20)
        user_circle.create_oval(2, 2, 33, 33, fill="#78909C", outline="")
        user_circle.create_text(17.5, 17.5, text="IG", fill="white", font=("Arial", 10, "bold"))

        # Main Content Section
        main_content = tk.Frame(self.frame, bg="#FCE4EC", padx=20, pady=20)
        main_content.pack(fill="x", pady=20)

        ai_powered_label = tk.Label(
            main_content,
            text="✨ AI-Powered",
            font=("Arial", 10, "bold"),
            bg="#FCE4EC",
            fg="#FF80AB"
        )
        ai_powered_label.pack(anchor="w")

        title_label = tk.Label(
            main_content,
            text="How can I help you today?",
            font=("Arial", 16, "bold"),
            bg="#FCE4EC",
            fg="#ffffff"
        )
        title_label.pack(anchor="w", pady=(5, 20))
        
        
        
        # Buttons Section
        buttons_frame = tk.Frame(main_content, bg="#FCE4EC")
        buttons_frame.pack()

        button_data = [
            ("📄 Generate Parent Update", "Create communication drafts", self.genParentUpdate),
            ("📊 Create IEP Report", "Auto-populate progress data", self.genIepReport),
            ("📚 Lesson Plan Ideas", "Standards-aligned suggestions", self.genLessonIdeas),
            ("❓ Answer Questions", "Assignment & due date info", self.genAnswers)
        ]

        for i, (title, subtitle, callback) in enumerate(button_data):
            button = tk.Frame(buttons_frame, bg="#FF80AB", padx=20, pady=10)
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

            title_label = tk.Button(
                button,
                text=title,
                font=("Arial", 12, "bold"),
                bg="#FF80AB",
                fg="white"
            )
            title_label.pack(anchor="w")

            subtitle_label = tk.Label(
                button,
                text=subtitle,
                font=("Arial", 10),
                bg="#FF80AB",
                fg="white"
            )
            subtitle_label.pack(anchor="w")

        # Recent AI Actions Section
        recent_actions_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        recent_actions_frame.pack(fill="x", pady=10)

        recent_title = tk.Label(
            recent_actions_frame,
            text="Recent AI Actions",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#212121"
        )
        recent_title.pack(anchor="w", pady=(0, 10))

        # hardcoded to make up for no users in app test
        actions = [
            ("✅ Generated 3 parent communication drafts", "2 hours ago"),
            ("✅ Answered 12 parent questions automatically", "Today"),
            ("✅ Updated IEP progress reports with classroom data", "Yesterday")
        ]

        for action, time in actions:
            action_frame = tk.Frame(recent_actions_frame, bg="#F5F5F5", padx=10, pady=10)
            action_frame.pack(fill="x", pady=5)

            action_label = tk.Button(
                action_frame,
                text=action,
                font=("Arial", 12, "bold"),
                bg="#FFFFFF",
                fg="#212121"
            )
            action_label.pack(anchor="w")

            time_label = tk.Label(
                action_frame,
                text=time,
                font=("Arial", 10),
                bg="#F5F5F5",
                fg="#757575"
            )
            time_label.pack(anchor="w")
    
        

    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()

# ========= Reports & Compliance Screen (Interactive Tabs) =========
class ReportsCompliancePage(tk.Frame):
    """Reports & Compliance screen UI, with interactive tabs."""
    def __init__(self, root, back_callback=None):
        super().__init__(root, bg="#f5f5f5")
        self.root = root
        self.back_callback = back_callback

        # State
        self.current_tab = "required"  # "required", "custom", "export"

        # Fake data for custom reports & exports
        self.custom_reports = [
            {
                "name": "Behavior Incidents Summary",
                "frequency": "Monthly",
                "format": "PDF"
            },
            {
                "name": "Reading Progress by Standard",
                "frequency": "Quarterly",
                "format": "CSV"
            },
            {
                "name": "Parent Contact Log",
                "frequency": "On-demand",
                "format": "PDF / CSV"
            },
        ]

        self.recent_exports = [
            {"name": "Monthly Attendance Log", "time": "Today 9:15 AM", "format": "Excel"},
            {"name": "Class Roster - Homeroom A", "time": "Yesterday", "format": "PDF"},
        ]

        # ====== HEADER ======
        header = tk.Frame(self, bg="#795548", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        branding_frame = tk.Frame(header, bg="#795548")
        branding_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            branding_frame,
            text="StreamlineEDU",
            font=("Arial", 14, "bold"),
            bg="#795548",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            branding_frame,
            text="Reports & Compliance",
            font=("Arial", 11),
            bg="#795548",
            fg="#D7CCC8"
        ).pack(anchor="w")

        # ====== NAV BAR ======
        nav_frame = tk.Frame(self, bg="#37474F", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        back_label = tk.Label(
            nav_frame,
            text="← Back  Reports",
            font=("Arial", 11),
            bg="#37474F",
            fg="white",
            cursor="hand2"
        )
        back_label.pack(side="left", padx=20)
        back_label.bind("<Button-1>", lambda e: self.on_back())

        # User circle (initials)
        user_canvas = tk.Canvas(
            nav_frame,
            width=35,
            height=35,
            bg="#37474F",
            highlightthickness=0
        )
        user_canvas.pack(side="right", padx=20)
        user_canvas.create_oval(2, 2, 33, 33, fill="#8D6E63", outline="")
        user_canvas.create_text(17.5, 17.5, text="IG", fill="white",
                                font=("Arial", 10, "bold"))

        # ====== TAB BAR ======
        tab_bar = tk.Frame(self, bg="white")
        tab_bar.pack(fill="x")

        tab_container = tk.Frame(tab_bar, bg="white")
        tab_container.pack(anchor="w", padx=20, pady=10)

        self.required_tab = tk.Label(
            tab_container,
            text="Required Reports",
            font=("Arial", 11),
            bg="white",
            fg="#795548",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.required_tab.pack(side="left", padx=(0, 15))
        self.required_tab.bind("<Button-1>", lambda e: self.switch_tab("required"))

        self.custom_tab = tk.Label(
            tab_container,
            text="Custom Reports",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.custom_tab.pack(side="left", padx=(0, 15))
        self.custom_tab.bind("<Button-1>", lambda e: self.switch_tab("custom"))

        self.export_tab = tk.Label(
            tab_container,
            text="Export",
            font=("Arial", 11),
            bg="white",
            fg="#757575",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.export_tab.pack(side="left")
        self.export_tab.bind("<Button-1>", lambda e: self.switch_tab("export"))

        # underline under active tab
        self.underline = tk.Frame(tab_container, bg="#795548", height=3, width=130)
        self.underline.place(x=10, y=30)

        # ====== SCROLLABLE CONTENT AREA ======
        content_outer = tk.Frame(self, bg="#f5f5f5")
        content_outer.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(content_outer, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(content_outer, orient="vertical",
                                 command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # optional: mouse wheel scroll
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # Render initial tab content
        self.render_content()

    # ---------- TAB LOGIC ----------

    def switch_tab(self, tab_name: str):
        """Switch between Required / Custom / Export tabs."""
        self.current_tab = tab_name

        # Update label colors
        self.required_tab.config(fg="#795548" if tab_name == "required" else "#757575")
        self.custom_tab.config(fg="#795548" if tab_name == "custom" else "#757575")
        self.export_tab.config(fg="#795548" if tab_name == "export" else "#757575")

        # Move underline (approx positions)
        positions = {
            "required": 10,
            "custom": 150,
            "export": 290
        }
        self.underline.place(x=positions[tab_name], y=30)

        # Rebuild content area
        self.render_content()

    def render_content(self):
        """Clear and rebuild the scroll frame based on active tab."""
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if self.current_tab == "required":
            self._create_compliance_section(self.scroll_frame)
            self._create_quick_exports_section(self.scroll_frame)
            self._create_info_banner(self.scroll_frame)
        elif self.current_tab == "custom":
            self._create_custom_reports_section(self.scroll_frame)
            self._create_info_banner(self.scroll_frame)
        elif self.current_tab == "export":
            self._create_export_tab_section(self.scroll_frame)

    # ---------- UI SECTION BUILDERS (REQUIRED TAB) ----------

    def _create_compliance_section(self, parent):
        container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        container.pack(fill="x", pady=(0, 15))

        # Section header
        header = tk.Frame(container, bg="white")
        header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header,
            text="Upcoming Compliance Deadlines",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")

        tk.Label(
            header,
            text="⚠️ 2 due soon",
            font=("Arial", 10),
            bg="white",
            fg="#E53935"
        ).pack(side="right")

        # ---- Card 1: Quarter 1 Progress Reports ----
        card1 = tk.Frame(container, bg="white")
        card1.pack(fill="x", padx=20, pady=(0, 10))

        left1 = tk.Frame(card1, bg="#E53935", width=4)
        left1.pack(side="left", fill="y", padx=(0, 10))

        c1 = tk.Frame(card1, bg="white")
        c1.pack(side="left", fill="both", expand=True, pady=10)

        top1 = tk.Frame(c1, bg="white")
        top1.pack(fill="x")

        tk.Label(
            top1,
            text="Quarter 1 Progress Reports",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")

        badge1 = tk.Label(
            top1,
            text="3 days left",
            font=("Arial", 9, "bold"),
            bg="#FFF3CD",
            fg="#856404",
            padx=8,
            pady=3
        )
        badge1.pack(side="right")

        tk.Label(
            c1,
            text="Due: November 15, 2025",
            font=("Arial", 10),
            bg="white",
            fg="#757575"
        ).pack(anchor="w", pady=(5, 10))

        tk.Button(
            c1,
            text="Auto-Generate Report",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self.simulate_auto_generate(
                "Quarter 1 Progress Reports"
            )
        ).pack(anchor="w")

        # ---- Card 2: Monthly Attendance Summary ----
        card2 = tk.Frame(container, bg="white")
        card2.pack(fill="x", padx=20, pady=(0, 10))

        left2 = tk.Frame(card2, bg="#4CAF50", width=4)
        left2.pack(side="left", fill="y", padx=(0, 10))

        c2 = tk.Frame(card2, bg="white")
        c2.pack(side="left", fill="both", expand=True, pady=10)

        top2 = tk.Frame(c2, bg="white")
        top2.pack(fill="x")

        tk.Label(
            top2,
            text="Monthly Attendance Summary",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")

        status_badge = tk.Label(
            top2,
            text="Ready",
            font=("Arial", 9, "bold"),
            bg="#D4EDDA",
            fg="#155724",
            padx=8,
            pady=3
        )
        status_badge.pack(side="right")

        tk.Label(
            c2,
            text="Due: November 30, 2025",
            font=("Arial", 10),
            bg="white",
            fg="#757575"
        ).pack(anchor="w", pady=(5, 0))

    def _create_quick_exports_section(self, parent):
        container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        container.pack(fill="x", pady=(0, 15))

        tk.Label(
            container,
            text="Quick Export Options",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 10))

        grid = tk.Frame(container, bg="white")
        grid.pack(fill="x", padx=20, pady=(0, 15))

        def export_btn(text, subtitle, row, col):
            btn = tk.Button(
                grid,
                text=f"{text}\n{subtitle}",
                font=("Arial", 10),
                justify="left",
                anchor="w",
                bg="#EEEEEE",
                fg="#212121",
                relief="flat",
                padx=12,
                pady=10,
                cursor="hand2",
                command=lambda: self.simulate_export(text, subtitle)
            )
            btn.grid(
                row=row,
                column=col,
                sticky="nsew",
                padx=(0, 10) if col == 0 else (0, 0),
                pady=(0, 10) if row == 0 else (0, 0)
            )

        export_btn("📄 Class Roster", "PDF / Excel", 0, 0)
        export_btn("📊 Grade Report", "PDF / CSV", 0, 1)
        export_btn("📅 Attendance Log", "Excel / PDF", 1, 0)
        export_btn("📝 IEP Summary", "PDF", 1, 1)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

    def _create_info_banner(self, parent):
        info_frame = tk.Frame(parent, bg="#FFF3E0", relief="solid", bd=1)
        info_frame.pack(fill="x")

        left = tk.Frame(info_frame, bg="#FFB74D", width=5)
        left.pack(side="left", fill="y")

        content = tk.Frame(info_frame, bg="#FFF3E0")
        content.pack(side="left", fill="x", expand=True, padx=15, pady=12)

        tk.Label(
            content,
            text="Automatic compliance:",
            font=("Arial", 10, "bold"),
            bg="#FFF3E0",
            fg="#212121",
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            content,
            text=(
                "System generates required reports on schedule and simulates "
                "submission to district systems automatically."
            ),
            font=("Arial", 10),
            bg="#FFF3E0",
            fg="#212121",
            anchor="w",
            wraplength=650,
            justify="left"
        ).pack(fill="x")

    # ---------- CUSTOM REPORTS TAB ----------

    def _create_custom_reports_section(self, parent):
        container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        container.pack(fill="x", pady=(0, 15))

        header = tk.Frame(container, bg="white")
        header.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header,
            text="Custom Reports",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121"
        ).pack(side="left")

        new_btn = tk.Button(
            header,
            text="+ New Custom Report",
            font=("Arial", 10),
            bg="#795548",
            fg="white",
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.create_custom_report
        )
        new_btn.pack(side="right")

        if not self.custom_reports:
            tk.Label(
                container,
                text="No custom reports defined yet.",
                font=("Arial", 10),
                bg="white",
                fg="#757575"
            ).pack(padx=20, pady=(0, 15))
            return

        for report in self.custom_reports:
            self._create_custom_report_card(container, report)

    def _create_custom_report_card(self, parent, report):
        card = tk.Frame(parent, bg="#FAFAFA", relief="solid", bd=1)
        card.pack(fill="x", padx=20, pady=(0, 10))

        inner = tk.Frame(card, bg="#FAFAFA")
        inner.pack(fill="x", padx=15, pady=10)

        # Title & metadata
        tk.Label(
            inner,
            text=report["name"],
            font=("Arial", 11, "bold"),
            bg="#FAFAFA",
            fg="#212121"
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=f"Frequency: {report['frequency']} • Format: {report['format']}",
            font=("Arial", 10),
            bg="#FAFAFA",
            fg="#757575"
        ).pack(anchor="w", pady=(2, 10))

        # Buttons
        btn_frame = tk.Frame(inner, bg="#FAFAFA")
        btn_frame.pack(anchor="w")

        tk.Button(
            btn_frame,
            text="Run Report",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2",
            command=lambda r=report: self.simulate_run_custom_report(r)
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame,
            text="Edit",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2",
            command=lambda r=report: self.simulate_edit_custom_report(r)
        ).pack(side="left")

    # ---------- EXPORT TAB ----------

    def _create_export_tab_section(self, parent):
        # Bulk export section
        bulk_container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        bulk_container.pack(fill="x", pady=(0, 15))

        tk.Label(
            bulk_container,
            text="Bulk Export",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 10))

        grid = tk.Frame(bulk_container, bg="white")
        grid.pack(fill="x", padx=20, pady=(0, 15))

        def bulk_btn(label, row, col):
            btn = tk.Button(
                grid,
                text=label,
                font=("Arial", 10),
                bg="#EEEEEE",
                fg="#212121",
                relief="flat",
                padx=12,
                pady=10,
                cursor="hand2",
                command=lambda: self.simulate_bulk_export(label)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=10, pady=5)

        bulk_btn("Export All Student Data", 0, 0)
        bulk_btn("Parent Contact List", 0, 1)
        bulk_btn("Compliance Archive (Year-to-Date)", 1, 0)
        bulk_btn("Download All Reports as ZIP", 1, 1)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # Recent exports
        recent_container = tk.Frame(parent, bg="white", relief="solid", bd=1)
        recent_container.pack(fill="x")

        tk.Label(
            recent_container,
            text="Recent Exports",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#212121",
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 10))

        if not self.recent_exports:
            tk.Label(
                recent_container,
                text="No exports yet. Run a report or use bulk export options above.",
                font=("Arial", 10),
                bg="white",
                fg="#757575"
            ).pack(padx=20, pady=(0, 15))
            return

        for exp in self.recent_exports:
            row = tk.Frame(recent_container, bg="white")
            row.pack(fill="x", padx=20, pady=5)

            info = tk.Frame(row, bg="white")
            info.pack(side="left", fill="x", expand=True)

            tk.Label(
                info,
                text=exp["name"],
                font=("Arial", 11),
                bg="white",
                fg="#212121",
                anchor="w"
            ).pack(anchor="w")

            tk.Label(
                info,
                text=f"{exp['time']} • {exp['format']}",
                font=("Arial", 9),
                bg="white",
                fg="#757575",
                anchor="w"
            ).pack(anchor="w")

            tk.Button(
                row,
                text="Download",
                font=("Arial", 9),
                bg="#2196F3",
                fg="white",
                relief="flat",
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda e=exp: self.simulate_download(e)
            ).pack(side="right")

    # ---------- INTERACTION / SIMULATION ----------

    def simulate_auto_generate(self, report_name: str):
        messagebox.showinfo(
            "Report Generated",
            f"{report_name} has been auto-generated.\n\n"
            "In a full version, this would create a PDF/CSV and submit "
            "it to the district system."
        )

        # Also add to recent exports list
        self.recent_exports.insert(0, {
            "name": report_name,
            "time": "Just now",
            "format": "PDF"
        })

    def simulate_export(self, label: str, subtitle: str):
        messagebox.showinfo(
            "Export Started",
            f"Simulated export started for:\n\n"
            f"{label}\nFormat options: {subtitle}"
        )
        self.recent_exports.insert(0, {
            "name": label,
            "time": "Just now",
            "format": subtitle
        })
        if self.current_tab == "export":
            self.render_content()

    def simulate_bulk_export(self, name: str):
        messagebox.showinfo(
            "Bulk Export",
            f"Simulated bulk export started for:\n\n{name}"
        )
        self.recent_exports.insert(0, {
            "name": name,
            "time": "Just now",
            "format": "ZIP" if "ZIP" in name else "Mixed"
        })
        if self.current_tab == "export":
            self.render_content()

    def simulate_run_custom_report(self, report: dict):
        messagebox.showinfo(
            "Custom Report Generated",
            f"{report['name']} has been generated.\n\n"
            f"Frequency: {report['frequency']}\nFormat: {report['format']}"
        )
        self.recent_exports.insert(0, {
            "name": report["name"],
            "time": "Just now",
            "format": report["format"]
        })
        if self.current_tab == "export":
            self.render_content()

    def simulate_edit_custom_report(self, report: dict):
        messagebox.showinfo(
            "Edit Custom Report",
            f"This would open an editor for:\n\n{report['name']}\n\n"
            "For now, this is a simulated interaction."
        )

    def create_custom_report(self):
        messagebox.showinfo(
            "New Custom Report",
            "This would walk you through creating a new custom report.\n\n"
            "For now, this is a simulated action."
        )

    def simulate_download(self, export_entry: dict):
        messagebox.showinfo(
            "Download",
            f"Pretending to download:\n\n{export_entry['name']}\n"
            f"Format: {export_entry['format']}\nTime: {export_entry['time']}"
        )

    def on_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            self.root.destroy()

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

# ========= Settings =========
class SettingsPage(tk.Frame):
    def __init__(self, root):
        
        super().__init__(root, bg = "#f5f5f5") 
        self.root = root
        self.root.title("Settings and Profile")
        self.root.configure(bg = "#f5f5f5")

        # Back button and Title:
        # Frame for button and title
        btFrame = tk.Frame(self, 
                           bg = "#1c1d42")
        btFrame.pack(fill = "x", 
                     pady = (10,0), 
                     padx = 10)

        # Back button
        backButton = tk.Button(btFrame, 
                               text = "← Back",
                               font=("Arial",14),
                               bg = "#1c1d42")
        backButton.pack(side = "left")

        # Page Title
        pageTitle = tk.Label(btFrame, 
                             text=f"Settings",
                             font=("Arial", 14, "bold"),
                             bg = "#1c1d42",
                             fg = "#f5f5f5")
        pageTitle.pack(side = "left", padx = 1)

        # Account Info (fake account to showcase code)
        accountUserPrefix = "Dr."
        accountUserFirstName = "Ivan"
        accountUserLastName = "Gappy"
        accountUserRole = "Teacher"
        accountGrade = "Grade 3" 
        accountSchool = "Maryville Elementary"

        #Profile Picture (placeholder)
        pfpCanvas = tk.Canvas(self, 
                              width=100, 
                              height=100, 
                              bg="#f5f5f5", 
                              highlightthickness=0)
        pfpCanvas.pack(pady=(10, 5))

        pfpCanvas.create_oval(10, 10, 90, 90, 
                              fill="#a5a5a5", 
                              outline="")

        pfpInitials = f"{accountUserFirstName[0]}{accountUserLastName[0]}"
        pfpCanvas.create_text(50, 50, 
                              text=pfpInitials, 
                              fill="white", 
                              font=("Arial", 30, "bold"))
        
        accountTitle = tk.Label(self, 
                                text=f"{accountUserPrefix} {accountUserFirstName} {accountUserLastName}",
                                font=("Arial", 20, "bold"),
                                bg = "#f5f5f5",
                                fg = "#1c1d42")
        accountTitle.pack(pady=(5, 0))

        accountInfoSubLabel = tk.Label(self, 
                                       text=f'{accountGrade} {accountUserRole} · {accountSchool}',
                                       font=("Arial", 15),
                                       bg = "#f5f5f5", 
                                       fg = "#7f8c8d")
        accountInfoSubLabel.pack(pady=(0, 10))

        

        # Account Settings frame
        asFrame = tk.Frame(self, 
                           width = 400, 
                           bg = "#e6e6e6")
        asFrame.pack(padx = 30, fill="x")
        asFrame.grid_columnconfigure(0, weight=1)
        asFrame.pack_propagate(False)
        
        asTitle = tk.Label(asFrame, 
                           text = "Account Settings",
                           font = ("Arial", 14, "bold"),
                           bg = "#e6e6e6",
                           fg = "#1c1d42")
        asTitle.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = (10, 5))

        # Profile Info Button
        profileInfoButton = tk.Button(asFrame, 
                                      text="Profile Information →",
                                      anchor="w",
                                      bg="#a5a5a5", fg = "gray",
                                      font=("Arial", 14, "bold"),
                                      padx=20, 
                                      pady = 10,
                                      relief="flat")
        profileInfoButton.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # class and student management button
        classStudentMngmntButton = tk.Button(asFrame, 
                                             text="Class & Student Management →",
                                             anchor="w",
                                             bg="#dedede", fg = "gray",
                                             font=("Arial", 14, "bold"),
                                             padx=20, 
                                             pady = 10,
                                             relief="flat")
        classStudentMngmntButton.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Notifications button
        notifButton = tk.Button(asFrame, 
                                text="Notifications →",
                                anchor="w",
                                bg="#a5a5a5", fg = "gray",
                                font=("Arial", 14, "bold"),
                                padx=20, 
                                pady = 10,
                                relief="flat")
        notifButton.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Integrations frame
        intFrame = tk.Frame(self, 
                            width = 400, 
                            bg = "#e6e6e6")
        intFrame.pack(padx = 30, pady=10, fill="x")
        intFrame.grid_columnconfigure(0, weight=1)
        intFrame.pack_propagate(False)

        intTitle = tk.Label(intFrame, 
                            text = "Integrations",
                            font = ("Arial", 14, "bold"),
                            bg = "#e6e6e6",
                            fg = "#1c1d42")
        intTitle.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = (10, 5))

        # Due to the nature of this test product, 
        districtSisConnection = False
        googleClassroomConnection = False

        # District SIS Button (is a frame)
        disSisFrame = tk.Frame(intFrame,
                               relief="flat",
                               bd=1,
                               bg="#f5f5f5")
        disSisFrame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        disSisFrame.grid_propagate(False)
        disSisTitle = tk.Label(disSisFrame,
                               text="District SIS",
                               font=("Arial", 14, "bold"),
                               bg="#f5f5f5", 
                               fg = "gray")
        disSisTitle.pack(side="left", padx=10, pady = 10)

        disSisStat = tk.Label(disSisFrame,
                              text = "Active" if districtSisConnection else "Inactive",
                              font = ("Arial", 12, "bold"),
                              fg = "green" if districtSisConnection else "red",
                              bg = "#69fc6e" if districtSisConnection else "#fe8d8d")
        disSisStat.pack(side="right",  padx=10, pady=10) 

        # Google Classroom button (also a frame)
        googleClassFrame = tk.Frame(intFrame,
                               relief="flat",
                               bd=1,
                               bg="#f5f5f5")
        googleClassFrame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        googleClassFrame.grid_propagate(False)
        googleClassTitle = tk.Label(googleClassFrame,
                               text="Google Classroom",
                               font=("Arial", 14, "bold"),
                               bg="#f5f5f5", 
                               fg = "gray")
        googleClassTitle.pack(side="left", padx=10, pady = 10)

        googleClassStat = tk.Label(googleClassFrame,
                              text = "Active" if googleClassroomConnection else "Inactive",
                              font = ("Arial", 12, "bold"),
                              fg = "green" if googleClassroomConnection else "red",
                              bg = "#69fc6e" if googleClassroomConnection else "#fe8d8d")
        googleClassStat.pack(side="right",  padx=10, pady=10)
       
        # AI Assistant frame
        aiAssistFrame = tk.Frame(self, 
                                 width = 400, 
                                 bg = "#e6e6e6")
        aiAssistFrame.pack(padx = 30, pady=10, fill="x")
        aiAssistFrame.grid_columnconfigure(0, weight=1)
        aiAssistFrame.pack_propagate(False)

        autoReportOnOff = tk.BooleanVar(value=True)
        iepGenOnOff = tk.BooleanVar(value=True)

        aiAssistTitle = tk.Label(aiAssistFrame, 
                                 text = "AI Assistant Preferences",
                                 font = ("Arial", 14, "bold"),
                                 bg = "#e6e6e6",
                                 fg = "#1c1d42")
        aiAssistTitle.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = (10, 5))

        # auto Report Button (is a frame)

        # Function for on off labels underneath button:
        def autoReportCbLabel():
            if autoReportOnOff.get():
                autoReportStat.config(text="On")
            else:
                autoReportStat.config(text="Off")


        autReportFrame = tk.Frame(aiAssistFrame,
                               relief="flat",
                               bd=1,
                               bg="#f5f5f5")
        
        autReportFrame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        #autReportFrame.grid_propagate(False)
        autReportFrame.columnconfigure(0, weight=1)

        autoReportTitle = tk.Label(autReportFrame,
                               text="Auto-generate parent communications",
                               font=("Arial", 14, "bold"),
                               bg="#f5f5f5", 
                               fg = "gray")
        
        autoReportTitle.grid(row=0, column=0, sticky="w", padx=10, pady=(8,0))

        autoReportSubLabel = tk.Label(autReportFrame, 
                                       text=f'AI will draft responses to parent communications',
                                       font=("Arial", 12),
                                       bg = "#f5f5f5", 
                                       fg = "#7f8c8d")
        autoReportSubLabel.grid(row= 1, column = 0, sticky= "w", padx=10, pady = (0,8))

        # Check Button
        autoReportToggleFrame = tk.Frame(autReportFrame,
                                         bg="#f5f5f5")
        autoReportToggleFrame.grid(row=0, column=1, rowspan=2, padx=10, pady=8)
        
        autoReportStat = tk.Label(autoReportToggleFrame,
                                  text="On",
                                  font="11",
                                  bg="#f5f5f5")
        
        autoReportStat.pack(side="bottom")
        
        autoReportCheck = tk.Checkbutton(autoReportToggleFrame,
                                         variable=autoReportOnOff,
                                         command=autoReportCbLabel,
                                         bg="#f5f5f5",
                                         activebackground="#f5f5f5")
        
        autoReportCheck.pack()

        # IEP Generation (also a frame)

        # Function for on off labels underneath button:
        def iepGenCbLabel():
            if iepGenOnOff.get():
                iepGenStat.config(text="On")
            else:
                iepGenStat.config(text="Off")

        iepGenFrame = tk.Frame(aiAssistFrame,
                               relief="flat",
                               bd=1,
                               bg="#f5f5f5")
        iepGenFrame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        #iepGenFrame.grid_propagate(False)
        iepGenFrame.columnconfigure(0, weight=1)
        iepGenTitle = tk.Label(iepGenFrame,
                               text="IEP Progress auto-population",
                               font=("Arial", 14, "bold"),
                               bg="#f5f5f5", 
                               fg = "gray")
        iepGenTitle.grid(row=0, column=0, sticky="w", padx=10, pady=(8,0))
        iepGenSubLabel = tk.Label(iepGenFrame, 
                                       text=f'Automatically generate IEP progress reports',
                                       font=("Arial", 12),
                                       bg = "#f5f5f5", 
                                       fg = "#7f8c8d")
        iepGenSubLabel.grid(row= 1, column = 0, sticky= "w", padx=10, pady = (0,8))


        # Check Button
        iepToggleFrame = tk.Frame(iepGenFrame,
                                  bg="#f5f5f5")
        iepToggleFrame.grid(row=0, column=1, rowspan=2, padx=10, pady=8)
        
        iepGenStat = tk.Label(iepToggleFrame,
                                  text="On",
                                  font="11",
                                  bg="#f5f5f5")
        
        iepGenStat.pack(side="bottom")
        
        iepGenCheck = tk.Checkbutton(iepToggleFrame,
                                         variable=iepGenOnOff,
                                         command=iepGenCbLabel,
                                         bg="#f5f5f5",
                                         activebackground="#f5f5f5")
        
        iepGenCheck.pack()

    def show(self):
        self.pack(fill="both", expand=True)
    def hide(self):
        self.pack_forget()

# ========= Main App Controller =========
class ClassroomManagementApp:
    """Main application controller"""
    def __init__(self, root):
        self.root = root
        self.root.title("StreamlineEDU - Classroom Management Platform")
        self.root.geometry("1200x700")  # Wider to fit 4 columns
        
        # Create screens
        self.login_screen = LoginScreen(root, self.show_dashboard)

        self.dashboard = DashboardScreen(
            root,
            self.show_lesson_planning,
            self.show_parent_communication,
            self.show_attendance,
            self.show_reports_compliance,
            self.show_iep_reports,
            self.show_settings,
            self.show_assessments,
            self.show_ai_assistant
        )
        self.lesson_planning = LessonPlanningScreen(root, self.show_dashboard)
        self.parent_communication = ParentCommunicationScreen(root, self.show_dashboard)
        self.attendance = AttendancePage(root, self.show_dashboard)
        self.reports_compliance = ReportsCompliancePage(root, self.show_dashboard)
        self.iep_reports = IEPProgressReportsScreen(root, self.show_dashboard)
        self.settings = SettingsPage(root)
        self.assessments = AssesmentsPage(root, self.show_dashboard)
        self.aiAssistant = AIAssistantScreen(root)
        
        # Show login by default
        self.show_login()

    def show_login(self):
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.dashboard.hide()
        self.settings.hide()
        self.login_screen.show()
    
    def show_dashboard(self):
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.dashboard.show()
        self.settings.hide()
        self.login_screen.hide()
        self.aiAssistant.hide()
    
    def show_lesson_planning(self):
        self.dashboard.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.lesson_planning.show()
    
    def show_parent_communication(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.parent_communication.show()

    def show_attendance(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.attendance.show()

    def show_reports_compliance(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.iep_reports.hide()
        self.reports_compliance.show()
    
    def show_iep_reports(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.show()

    def show_settings(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.settings.show()

    def show_assessments(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.settings.hide()
        self.assessments.show()

    def show_ai_assistant(self):
        self.dashboard.hide()
        self.lesson_planning.hide()
        self.parent_communication.hide()
        self.attendance.hide()
        self.reports_compliance.hide()
        self.iep_reports.hide()
        self.settings.hide()
        self.assessments.hide()
        self.aiAssistant.show()

# Launches App :)
if __name__ == "__main__":
    root = tk.Tk()
    app = ClassroomManagementApp(root)
    root.mainloop()
