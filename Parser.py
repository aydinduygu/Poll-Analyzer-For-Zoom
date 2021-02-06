import pandas as pd
import datetime
from TR_Text import tr_upper, tr_lower
import locale
import re

# -*- coding: utf-8 -*-
from StringComparator import StringComparator
from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question
from OutputProducer import OutputProducer
from pathlib import Path


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

        #locale.setlocale(locale.LC_COLLATE,'C')

        self.__stuNotCorrelated = []
        self.__dataNotCorrelated = {}
        self.__dataCorrelated={}


    def binarySearchStuList(self,string: str,studentList):

        l = 0
        r = len(studentList) - 1

        while (l <= r):

            m = int((l + r) / 2)
            string2 = studentList[m].getName() + " " + studentList[m].getSurname()

            strcmp=StringComparator(string,string2).cmp_ig_C_S_P_N

            if (strcmp==0):
                return m
            elif (strcmp==1):
                l = m + 1
            else:
                r = m - 1
        return -1  # If element is not found  then it will return -1


    def parseQuizes(self,answerSheetAsList):

        indexList=[index for index,value in enumerate(answerSheetAsList)
                   if value.lower().__contains__("question") and value.lower().__contains__("poll")]


        try:
            polls = [answerSheetAsList[val:indexList[i + 1]] for i, val in enumerate(indexList) if indexList[i]!=indexList[-1] and answerSheetAsList[val]!='\n']
        except :
            pass

        questions=[]

        try:
            for i,poll in enumerate(polls):
                pollInfos=re.split('[\n\t]',poll[0])
                qz=Quiz(None,None)
                qz.setQuizName(pollInfos[0])
                qz.setNumOfQuestions(int(pollInfos[1][0]))
                polls[polls.index(poll)]=[item for item in poll if item!="\n"]
                poll=polls[i]
                poll=poll[1:]
                indexList2 = [index for index, value in enumerate(poll) if
                              not value[0:9].lower().__contains__("answer")]

                q_dict={}
                qText=""
                for item in poll:

                    if item.__contains__('\n'):
                        item = item.replace('\n', '')

                    if not item[0:9].lower().__contains__("answer"):

                        item=item[2:]


                        if item.__contains__('( Single Choice)'):
                            item = item.replace('( Single Choice)', '')
                        if item.__contains__('( Multiple Choice)'):
                            item = item.replace('( Multiple Choice)', '')
                        item=item.strip()
                        q_dict[item]=[]
                        qText=item
                    else:

                        item=item.replace('Answer','')
                        item=item[3:]

                        q_dict[qText].append(item)

                for key in q_dict.keys():
                    q=Question(None,key,q_dict[key])
                    questions.append(q)


        except :
            pass
        
        questions=sorted(questions)
        return questions

    def binarySearchQuestions(self,question,questions):
        l = 0
        r = len(questions) - 1

        while (l <= r):

            m = int((l + r) / 2)


            if (questions[m] == question):
                return questions[m]
            elif (question>questions[m]):
                l = m + 1
            else:
                r = m - 1
        return -1  # If element is not found  then it will return -1



    def parse(self, filePath,paths, columnNames,answerKeyPaths,updateBar):

        studentList=self.parseStudentList(filePath,columnNames["name"], columnNames["surname"],columnNames["id"])

        answerKeys=[]
        quizes={}

        self.__oProducer.addIntoExecutionLog("Answer Sheets: "+str(answerKeyPaths)+" are  being parsed")
        for path in answerKeyPaths:

            file = open(path, 'r')
            lines = file.readlines()
            answerKeys.append(self.parseQuizes(lines))

        self.__oProducer.addIntoExecutionLog("Answer Sheets have been parsed.")

        quizNameList={}
        for myindex,path in enumerate(paths):

            updateBar(int(50/len(paths)))

            self.__oProducer.addIntoExecutionLog("Poll file: "+path+" is being parsed")

            #get first 5 lines of csv
            df_head=pd.read_table(Path(path),skiprows=2,nrows=1,error_bad_lines=False,sep=',')

            quizName=self.__parseColumn(df_head,'Topic')[0]

            #get after 5 lines
            df = pd.read_csv(Path(path), skiprows=5,index_col=False,error_bad_lines=False)

            #detect column numbers of username, email and datetime strings
            uName_cIndex = df.columns.get_loc(columnNames["username"])
            email_cIndex = df.columns.get_loc(columnNames["email"])
            date_cIndex = df.columns.get_loc(columnNames["datetime"])

            #read after 6 lines
            df = pd.read_csv(Path(path), skiprows=6, index_col=False,header=None,error_bad_lines=False)

            #detect number of rows and number of columns
            numColumn = len(df.columns)
            numRow = len(df.index)

            #list of index numbers of questions
            q_IndexList = [x for x in range(date_cIndex + 1, numColumn - 1) if x % 2 == 0]

            #list of index numbers of student responds
            a_IndexList = [x for x in range(date_cIndex + 1, numColumn - 1) if x % 2 != 0]

            #list row indexes of lines with attendence question
            indexNames = df[df[df.columns[date_cIndex + 3]].isnull()].index

            #generate an empty dataframe to keep inassociated data after method ended
            self.__dataNotCorrelated[path] = pd.DataFrame(columns=df.columns.tolist())

            #extract class dates as different dataframe
            df_clsDates = df.copy(deep=True)
            df_clsDates = pd.DataFrame(df[df.columns[date_cIndex]].str.split(" ", 3).tolist(),columns=["month", "day", "year", "time"])
            df_clsDates = pd.DataFrame(df_clsDates["month"] + " " + df_clsDates["day"] + " " + df_clsDates["year"])
            df_clsDates = df_clsDates.drop_duplicates(keep="first")

            #extract lines with attencence question(lines with the column that is 3 after from date column is null)
            df_att = df.loc[df[df.columns[date_cIndex + 3]].isnull()]
            df_att = df_att.reset_index(drop=True)
            df = df.reset_index(drop=True)

            # list indexes of lines with the attendence question
            dfattList = list(df_att.index)

            #add class dates into attendence attributes of all students
            for index, row in df_clsDates.iterrows():

                myClsdatetime = str(row.loc[0])
                myClsdatetime = datetime.datetime.strptime(myClsdatetime, "%b %d, %Y")

                for stu in studentList\
                        :
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

                    stuIndex = self.binarySearchStuList(username,studentList)

                    if stuIndex != -1:
                        stu = studentList[stuIndex]

                        if stu.getUsername() == None:
                            stu.setUsername(username)
                        if stu.getEmail() == None:
                            stu.setEmail(email)
                        stu.getAttendence().add_Attendence(mydatetime.date())


                    else:
                        stu = None

                        r = df_att.iloc[index, :]
                        self.__dataNotCorrelated[path].loc[index] = row.transpose()
            if b!=0:
                if not quizName in quizNameList:
                    quizNameList[quizName] = 1
                else:
                    quizNameList[quizName] += 1

            for index, row in df.iterrows():

                username = str(row.loc[df.columns[uName_cIndex]])
                email = str(row.loc[df.columns[email_cIndex]])
                mydatetime = str(row.loc[df.columns[date_cIndex]])
                mydatetime = datetime.datetime.strptime(mydatetime, "%b %d, %Y %H:%M:%S")

                stuIndex = self.binarySearchStuList(username,studentList)

                if stuIndex != -1:
                    stu = studentList[stuIndex]

                    if stu.getUsername() == None:
                        stu.setUsername(username)
                    if stu.getEmail() == None:
                        stu.setEmail(email)

                    qpList = []
                    i = 1

                    qz = Quiz(None, mydatetime.date())
                    for c in q_IndexList:
                        q = Question(i, str(row.loc[df.columns[c]]), "")

                        for ansKey in answerKeys:
                            q2=self.binarySearchQuestions(q,ansKey)
                            if q2!=-1:
                                q2.setQuestionNumber(i)
                                q=q2
                                break

                        responds=str(row.loc[df.columns[c + 1]]).split(sep=';')
                        qp = QuizPart(q, responds)

                        isRespondCorrect=False
                        for r in responds:

                            for a in q.getAnswer():

                                strcmp=StringComparator(r,a).cmp_ig_CaseSpacePunc

                                if strcmp==0:
                                    qp.setIsCorrect(1)
                                    qz.setNumCorrect(qz.getNumCorrect()+1)
                                    isRespondCorrect=True
                                    break

                            if isRespondCorrect:
                                break




                        if not isRespondCorrect:
                            qz.setNumWrong(qz.getNumWrong()+1)


                        qpList.append(qp)
                        i+=1

                    qz.setQuizParts(qpList)
                    stu.getQuizes().append(qz)

                    for quiz in stu.getQuizes():
                        if quiz.getQuizName()==(quizName+"_"+str(quizNameList[quizName])):
                            quizNameList[quizName]+=1

                    qz.setQuizName(quizName+"_"+str(quizNameList[quizName]))


                    #stu.getQuizes()[stu.getQuizes().index(qz)].setQuizName("quiz"+str(stu.getQuizes().index(qz)))


                    stu.getAttendence().add_Attendence(mydatetime.date())


                else:
                    stu = None
                    self.__dataNotCorrelated[path].loc[index] = row.transpose()

            self.__dataNotCorrelated[path].drop(self.__dataNotCorrelated[path].columns[0], axis=1, inplace=True)
            self.__dataNotCorrelated[path] = self.__dataNotCorrelated[path].reset_index(drop=True)
            self.__dataNotCorrelated[path] = self.__dataNotCorrelated[path].reindex()
            self.__oProducer.addIntoExecutionLog("Parsing of Poll file: " + path + " ended.")

        self.detectUncorStu(studentList)
        return studentList,self.__dataNotCorrelated,self.__stuNotCorrelated



    def detectUncorStu(self,studentList):

        self.__oProducer.addIntoExecutionLog("Looking up for anomalies...")
        self.__stuNotCorrelated = [stu for stu in studentList
                                   if stu.getUsername() == None]
        self.__oProducer.addIntoExecutionLog("Anomaly detection ended!")


    def parseStudentList(self, filePath, name: str, surname: str, id: str):
        self.__oProducer.addIntoExecutionLog("Parsing Student List started : " + filePath + " started")

        df = pd.read_excel(filePath, header=12)
        nameList = self.__parseColumn(df, name)
        surnameList = self.__parseColumn(df, surname)
        studentIdList = self.__parseColumn(df, id)

        studentList = []
        locale.setlocale(locale.LC_COLLATE,locale="tr-TR")

        for x in range(0, len(studentIdList)):
            name = tr_upper(str(nameList[x]))
            surname = tr_upper(str(surnameList[x]))
            studentId=studentIdList[x]
            stu = Student(name, surname, studentId)
            studentList.append(stu)

        self.__oProducer.addIntoExecutionLog("Parsing Student List : " + filePath + " finished")

        letters = "abcçdefgğhıijklmnoöprsştuüvyz"
        d = {i: letters.index(i) for i in letters}

        studentList=sorted(studentList)

        return studentList

    def __parseColumn(self, df, columName):
        df = df[columName]
        df = df.dropna()
        df = df.values
        nameList = []
        nameList.extend(df)
        nameList = [x for x in nameList if x != columName]

        return nameList


    def getStuNotCor(self):
        return self.__stuNotCorrelated

    def getDataNotCor(self):
        return self.__dataNotCorrelated