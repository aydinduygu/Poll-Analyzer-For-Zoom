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

    def parseStudentList(self):
        df = pd.read_excel(self.__filePath1, header=12)
        nameList = self.parseColumn(df, "Adı")
        surnameList = self.parseColumn(df, "Soyadı")
        studentIdList = self.parseColumn(df, "Öğrenci No")

        studentList = []

        for x in range(0, len(studentIdList)):
            stu = Student(nameList[x], surnameList[x], studentIdList[x])
            studentList.append(stu)

        return studentList

    def parseColumn(self, df, columName):
        df = df[columName]
        df = df.dropna()
        df = df.values
        nameList = []
        nameList.extend(df)
        nameList = [x for x in nameList if x != columName]

        return nameList
