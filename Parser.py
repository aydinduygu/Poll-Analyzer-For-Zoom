import pandas as pd

from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question


class Parser:
    __filePath1 = ""
    __filePath2 = ""

    def __init__(self, filePath1, filePath2):
        self.__filePath1 = filePath1
        self.__filePath2 = filePath2

    def parsestudentlist(self):
        df = pd.read_excel(self.__filePath1)
        print(df)
