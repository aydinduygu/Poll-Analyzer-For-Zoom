from Quiz import Quiz

class Student:
    name = ""
    surname = ""
    student_id = 0
    attendance = 0

    def __init__(self, name, surname, student_id):
        self.name = name
        self.surname = surname
        self.student_id = student_id
