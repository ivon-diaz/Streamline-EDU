"""
This code shows what information would be pulled from pre-existing data within the application 
to complete reports

"""
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

class AttendanceRecord:
    def __init__(self, student_id, date, present: bool):
        self.student_id = student_id
        self.date = date
        self.present = present

class Assessment:
    def __init__(self, student_id, date, score):
        self.student_id = student_id
        self.date = date
        self.score = score

class IEPGoal:
    def __init__(self, student_id, description, target_score):
        self.student_id = student_id
        self.description = description
        self.target_score = target_score

def generate_attendance_report(student, attendance_records):
    #calculate %
    ...

def generate_assessment_report(student, assessments):
    # calculate avg score
    ...

def generate_iep_progress(student, assessments, iep_goals):
    # compare scores to goals and return a summary paragraph
    ...
