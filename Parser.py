import pandas as pd

from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question


class Parser:
    filePath1 = ""
    filePath2 = ""

    def __init__(self, filePath1, filePath2):
        self.filePath1 = filePath1
        self.filePath2 = filePath2

    def parsestudentlist(self):
        df = pd.read_excel(self.filePath1)
        print(df)
