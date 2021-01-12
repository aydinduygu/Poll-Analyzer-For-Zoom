import pandas as pd

import Student
import Quiz
import QuizPart
import Question


class Parser:
    filePath1 = ""
    filePath2 = ""

    def __init__(self, filePath1, filePath2):
        self.filePath1 = filePath1
        self.filePath2 = filePath2

    def parsestudentlist(self):
        df = pd.read_excel(self.filePath1)
        print(df)
