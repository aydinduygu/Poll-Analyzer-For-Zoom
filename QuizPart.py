from Question import Question


class QuizPart:
    question = None
    student_respond = None

    def __init__(self, question, student_respond):
        self.question = question
        self.student_respond = student_respond
