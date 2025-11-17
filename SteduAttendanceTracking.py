import tkinter as tk
from tkinter import ttk
from datetime import date

class AttendancePage(tk.Frame):
    

    def __init__(self, root):
        super().__init__(root, bg = "#f5f5f5") 
        self.root = root
        self.root.title("Attendance")            #
        self.root.geometry("600x700")            # Matching other pages
        self.root.configure(bg = "#f5f5f5")      #

        # Back button
        backButton = tk.Button(self, text = "← Back",
                               font=("Arial",14),
                               relief = "flat")
        backButton.pack(anchor="w", pady = (10, 0), padx = 10)

        # Page title
        gradeLevel = "temp" # placeholder grade

        pageTitle = tk.Label(self, text=f"Attendance - Grade {gradeLevel}",
                             font=("Arial", 20, "bold"), bg = "#063563")
        pageTitle.pack(pady=(5, 0))

        # Date
        attFullDate = date.today() # gets full date

        attWeekdayInt = attFullDate.weekday() # gets the weekday as an int
        attWeekdayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] # list of weekdays
        attWeekday = attWeekdayList[attWeekdayInt] # converts weekday int into weekday

        attMonth = attFullDate.month # gets the month
        attDay = attFullDate.day # gets the day
        attYear = attFullDate.year # gets the year
        
        dateLabel = tk.Label(self, text= f"{attWeekday}, {attMonth} {attDay}, {attYear}",
                             font= ("Arial", 12, "bold"), bg="#f5f5f5", 
                             fg="#2c3e50")
        
        dateLabel.pack(pady=(10,0))

        # Enrolled Students

        enrollmentLabel = tk.Label(self, text="X students enrolled",
                                   font=("Arial", 10),
                                   bg="#f5f5f5", fg = "#7f8c8d")
        
        enrollmentLabel.pack(pady=(0, 10))

        # Attendance list

        self.attVars = {}
        students = ["Jordan Rashid", "Ivon Diaz", "Hadi Khan", "Marcus Johnson", "Olivia Martinez"]

        for student in students:
            frame = tk.Frame(self, bg="white", relief="solid", bd=1)
            frame.pack(fill="x", padx=10, pady=5)

            nameLabel = tk.Label(frame, text=student, font=("Arial", 12, "bold"), 
                                 bg="white", fg="#2C3E50")
            nameLabel.pack(side="left", padx=10, pady=5)

            var = tk.StringVar(value="Present")
            self.attendance_vars[student] = var

            presentButton = tk.Radiobutton(frame, text="Present", 
                                           variable=var, value="Present", 
                                           bg="white", fg="#27AE60", 
                                           font=("Arial", 10))
            
            presentButton.pack(side="right", padx=5)

            absentButton = tk.Radiobutton(frame, text="Absent", 
                                          variable=var, value="Absent", 
                                          bg="white", fg="#E74C3C", 
                                          font=("Arial", 10))
            

            absentButton.pack(side="right", padx=5)

        # Submit button
        submitButton = tk.Button(self, text="Submit to District",
                                 bg="#1aaf78", fg = "white",
                                 font=("Arial", 14, "bold"),
                                 padx=20, pady = 10,
                                 relief="flat")
        
        submitButton.pack(pady = 20)

        # Submit button functions
    def submitAtt(self):
        attData = {student: var.get() for student, var in self.attVars.items()}
        print(f"Attendance: {attData}")

if __name__ == "__main__":
    root = tk.Tk()
    page = AttendancePage
    page.pack(fill="both", expand=True)
    root.mainLoop()





