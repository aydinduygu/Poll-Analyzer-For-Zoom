import pandas as pd
import openpyxl
import datetime
import time
import math
import operator
from TR_Text import tr_upper, tr_lower
import locale

# -*- coding: utf-8 -*-
from StringComparator import StringComparator
from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question
from OutputProducer import OutputProducer



class Parser:
    __oProducer = None
    __correlator = None
    __studentList = None
    __stuNotCorrelated = None
    __dataNotCorrelated = None
    __dataCorrelated=None

    def __init__(self, xls_filePath, csv_filePaths,answerKeys, columnNames):

        #locale.setlocale(locale.LC_COLLATE, "tr_TR")

        self.__oProducer = OutputProducer.instance()
        self.__studentList = self.parseStudentList(xls_filePath, columnNames["name"], columnNames["surname"],
                                                   columnNames["id"])
        self.__studentList.sort(key=lambda x: tr_lower(x.getName()) + tr_lower(x.getSurname()))
        self.__studentList=sorted(self.__studentList, key=lambda x: locale.strxfrm(tr_lower(x.getName())+tr_lower(x.getSurname())))
        #locale.setlocale(locale.LC_COLLATE,'C')
        self.__stuNotCorrelated = []
        self.__dataNotCorrelated = {}
        self.__dataCorrelated={}
        self.parse(csv_filePaths, columnNames, "Are you attending this lecture?")
        self.parseAnswerKey(answerKeys,self.__studentList)


    def linearSearchStuList(self, string: str):


        for m in range(len(self.__studentList)):

            string2 = self.__studentList[m].getName() + " " + self.__studentList[m].getSurname()

            res = StringComparator(string, string2).cmp_ig_C_S_P_N

            if res == 0:
                return m

        return -1

    def parse(self, paths, columnNames, attendenceQuestion):

        for path in paths:
            df = pd.df = pd.read_csv(path)

            uName_cIndex = df.columns.get_loc(columnNames["username"])
            email_cIndex = df.columns.get_loc(columnNames["email"])
            date_cIndex = df.columns.get_loc(columnNames["datetime"])

            df = pd.read_csv(path, skiprows=1, header=None)
            df_att = df.loc[df[df.columns[date_cIndex + 1]].isin([attendenceQuestion])]
            df_att = df_att.reset_index(drop=True)
            df = df.reset_index(drop=True)

            numColumn = len(df.columns)
            numRow = len(df.index)

            q_IndexList = [x for x in range(date_cIndex + 1, numColumn - 1) if x % 2 == 0]
            a_IndexList = [x for x in range(date_cIndex + 1, numColumn - 1) if x % 2 != 0]

            dfattList = list(df_att.index)
            indexNames = df[df[df.columns[date_cIndex + 1]] == attendenceQuestion].index
            self.__dataNotCorrelated[path] = pd.DataFrame(columns=df.columns.tolist())

            df_clsDates = df.copy(deep=True)

            df_clsDates = pd.DataFrame(df[df.columns[date_cIndex]].str.split(" ", 3).tolist(),
                                       columns=["month", "day", "year", "time"])
            df_clsDates = pd.DataFrame(df_clsDates["month"] + " " + df_clsDates["day"] + " " + df_clsDates["year"])
            df_clsDates = df_clsDates.drop_duplicates(keep="first")

            for index, row in df_clsDates.iterrows():

                myClsdatetime = str(row.loc[0])
                myClsdatetime = datetime.datetime.strptime(myClsdatetime, "%b %d, %Y")

                for stu in self.__studentList:
                    stu.getAttendence().add_clsDate(myClsdatetime.date())

            a = len(df.index)
            df.drop(indexNames, inplace=True, axis=0)
            b = len(df.index)

            if a > b:

                j = 0
                for index, row in df_att.iterrows():
                    username = str(row.loc[df_att.columns[uName_cIndex]])
                    email = str(row.loc[df_att.columns[email_cIndex]])
                    mydatetime = str(row.loc[df_att.columns[date_cIndex]])
                    mydatetime = datetime.datetime.strptime(mydatetime, "%b %d, %Y %H:%M:%S")

                    stuIndex = self.linearSearchStuList(username)

                    if stuIndex != -1:
                        stu = self.__studentList[stuIndex]

                        if stu.getUsername() == None:
                            stu.setUsername(username)
                        if stu.getEmail() == None:
                            stu.setEmail(email)
                        stu.getAttendence().add_Attendence(mydatetime.date())


                    else:
                        stu = None

                        r = df_att.iloc[index, :]
                        self.__dataNotCorrelated[path].loc[index] = row.transpose()

            for index, row in df.iterrows():

                username = str(row.loc[df.columns[uName_cIndex]])
                email = str(row.loc[df.columns[email_cIndex]])
                mydatetime = str(row.loc[df.columns[date_cIndex]])
                mydatetime = datetime.datetime.strptime(mydatetime, "%b %d, %Y %H:%M:%S")

                stuIndex = self.linearSearchStuList(username)

                if stuIndex != -1:
                    stu = self.__studentList[stuIndex]

                    if stu.getUsername() == None:
                        stu.setUsername(username)
                    if stu.getEmail() == None:
                        stu.setEmail(email)

                    qpList = []
                    i = 1
                    for c in q_IndexList:
                        q = Question(i, str(row.loc[df.columns[c]]), "")

                        answers=str(row.loc[df.columns[c + 1]]).split(sep=';')


                        qp = QuizPart(q,answers)
                        qpList.append(qp)
                        i+=1

                    qz = Quiz(qpList, mydatetime.date())


                    stu.getQuizes().append(qz)
                    stu.getQuizes()[stu.getQuizes().index(qz)].setQuizName("quiz"+str(stu.getQuizes().index(qz)))


                    stu.getAttendence().add_Attendence(mydatetime.date())


                else:
                    stu = None
                    self.__dataNotCorrelated[path].loc[index] = row.transpose()

            self.__dataNotCorrelated[path].drop(self.__dataNotCorrelated[path].columns[0], axis=1, inplace=True)
            self.__dataNotCorrelated[path] = self.__dataNotCorrelated[path].reset_index(drop=True)
            self.__dataNotCorrelated[path] = self.__dataNotCorrelated[path].reindex()

        self.detectUncorStu()



    def detectUncorStu(self):

        self.__stuNotCorrelated = [stu for stu in self.__studentList if stu.getUsername() == None]

    def parseStudentList(self, filePath, name: str, surname: str, id: str):
        self.__oProducer.addIntoExecutionLog("Parsing Student List started : " + filePath + " started")

        df = pd.read_excel(filePath, header=12)
        nameList = self.__parseColumn(df, name)
        surnameList = self.__parseColumn(df, surname)
        studentIdList = self.__parseColumn(df, id)

        studentList = []

        for x in range(0, len(studentIdList)):
            name = tr_lower(str(nameList[x]))
            surname = tr_lower(str(surnameList[x]))
            stu = Student(name, surname, studentIdList[x])
            studentList.append(stu)

        self.__oProducer.addIntoExecutionLog("Parsing Student List : " + filePath + " finished")

        return studentList

    def __parseColumn(self, df, columName):
        df = df[columName]
        df = df.dropna()
        df = df.values
        nameList = []
        nameList.extend(df)
        nameList = [x for x in nameList if x != columName]

        return nameList



    def parseAnswerKey(self, paths, studentList):

        for path2 in paths:
            df_withHeader = pd.read_excel(path2)
            quizName = df_withHeader.columns[0]

            df_answerKey = pd.read_excel(path2, skiprows=1, header=None)
            questionList = df_answerKey.iloc[:, 0]
            answerList = df_answerKey.iloc[:, 1]

            qlist = []
            alist = []
            questionList = questionList.values
            answerList = answerList.values

            qlist.extend(questionList)
            alist.extend(answerList)

            numRows = len(df_answerKey.index)

            length = len(studentList)
            length2 = 0
            length3 = 0

            for i in range(length):
                length2 = len(studentList[i].getQuizes())
                for j in range(length2):
                    length3 = len(studentList[i].getQuizes()[j].getQuizParts())
                    for k in range(length3):

                        for m in range(numRows):

                            string1=studentList[i].getQuizes()[j].getQuizParts()[k].getQuestion().getQuestionText()
                            string2=qlist[m]

                            match=StringComparator(string1,string2).cmp_ig_C_S_P_N
                            if match==0:

                                studentList[i].getQuizes()[j].getQuizParts()[k].getQuestion().setAnswer(alist[m].split(sep=';'))


    def getStudentList(self):
        return self.__studentList

    def getStuNotCor(self):
        return self.__stuNotCorrelated

    def getDataNotCor(self):
        return self.__dataNotCorrelated