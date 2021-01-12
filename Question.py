class Question:
    question_id = None
    question_text = None
    answer = None

    def __init__(self, question_id, question_text, answer):
        self.question_id = question_id
        self.question_text = question_text
        self.answer = answer
