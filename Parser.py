import pandas as pd
import openpyxl

# -*- coding: utf-8 -*-
from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question
from OutputProducer import  OutputProducer


class Parser:

    __oProducer=None

    def __init__(self):

        self.__oProducer = OutputProducer.instance()

        pass

    def parseStudentList(self, filePath):
        self.__oProducer.addIntoExecutionLog("Parsing Student List started : " + filePath + " started")
        df = pd.read_excel(filePath, header=12)
        nameList = self.parseColumn(df, "Adı")
        surnameList = self.parseColumn(df, "Soyadı")
        studentIdList = self.parseColumn(df, "Öğrenci No")

        studentList = []

        for x in range(0, len(studentIdList)):

            name=str(nameList[x])

            surname=str(surnameList[x])



            name=self.adjustString(name)
            surname=self.adjustString(surname)

            asc = [ord(c) for c in name]
            asc2 = [ord(c) for c in surname]


            name=name.lower()
            surname=surname.lower()

            stu = Student(name, surname, studentIdList[x])
            studentList.append(stu)
        self.__oProducer.addIntoExecutionLog("Parsing Student List : " + filePath + " finished")
        return studentList

    def parseColumn(self, df, columName):
        df = df[columName]
        df = df.dropna()
        df = df.values
        nameList = []
        nameList.extend(df)
        nameList = [x for x in nameList if x != columName]

        return nameList

    def parseAttendance(self, path):

        self.__oProducer.addIntoExecutionLog("Parsing attendence : " + path + " started")
        global a

        a=-1
        df = pd.read_csv(r'{}'.format(path))
        df.reset_index(inplace=True)

        for i in df.columns:
            try:
                if df[df[i].str.contains('Are you attending this lecture?')].shape[0] > 0:
                    a = i

            except:
                pass

        if a!=-1:
            attendance = df[df[a].str.contains('Are you attending this lecture?')]
            attendance = attendance[attendance.columns[1:6]]
            attendance.columns = ['User Name', 'User Mail', 'Submitted Date/Time', 'Q', 'A']
            attendance.rename(columns={'A': attendance['Q'].unique()[0]}, inplace=True)
            attendance.reset_index(drop=True, inplace=True)
            attendance.drop('Q', axis=1, inplace=True)

            attendanceList = []

            attendance = attendance['User Name']
            attendanceList.extend(attendance)
            self.__oProducer.addIntoExecutionLog("Parsing attendence : " + path + " finished")

            return attendanceList

    def adjustString(self, userName:str):

        for s in userName:
            if s.isdigit() == True:
                userName = userName.replace(s, '')
        userName = userName.strip()
        

        if userName.__contains__("  "):
            userName.replace("  "," ")

        if userName.__contains__("İ"):
            userName = userName.replace("İ", "i")
        if userName.__contains__("I"):
            userName=userName.replace("I","ı")
        if userName.__contains__("Ü"):
            userName = userName.replace("Ü", "ü")
        if userName.__contains__("Ğ"):
            userName = userName.replace("Ğ", "ğ")
        if userName.__contains__("Ş"):
            userName = userName.replace("Ş", "ş")
        if userName.__contains__("Ç"):
            userName = userName.replace("Ç", "ç")
        if userName.__contains__("Ö"):
            userName = userName.replace("Ö", "ö")
        userName=userName.lower()
        return userName


    def parseQuiz(self, path1, studentList):

        global qText
        self.__oProducer.addIntoExecutionLog("Parsing quiz file : "+path1+" started")

        df_quiz = pd.read_csv(path1, skiprows=1, header=None)


        numCol = len(df_quiz.columns)
        numRows = len(df_quiz.index)
        q_IndexList = [x for x in range(4, numCol - 1) if x % 2 == 0]
        a_IndexList = [x for x in range(4, numCol - 1) if x % 2 != 0]

        questions = df_quiz[df_quiz.columns[q_IndexList]]
        answers = df_quiz[df_quiz.columns[a_IndexList]]

        qNum = 1

        for x in range(0, numRows):

            myatq = df_quiz.iloc[x][4]

            if myatq == "Are you attending this lecture?":
                continue
            else:
                quizPartList = []
                qNum=1

                for y in q_IndexList:
                    qText = questions.iloc[x][y]
                    
                    if str(qText)!="nan":
                        qText = self.checkQuestion(qText)
                            
                    q = Question(qNum, qText, "")
                    aText = answers.iloc[x][y + 1]
                    qp = QuizPart(q, aText)
                    quizPartList.append(qp)
                    qNum=qNum+1


                quiz = Quiz(quizPartList)

                userName = df_quiz.iloc[x][1]
                if userName.isalpha() == False:
                    userName = self.adjustString(userName)
                    df_quiz.at[x, 1] = userName

                i = -1

                for stu in studentList:

                    s_name=self.adjustString(str(stu.getName()))
                    s_surname=self.adjustString(str(stu.getSurname()))
                    s_username=s_name+" "+s_surname
                    s_username=self.adjustString(s_username)
                    asci2=[ord(c) for c in s_username]
                    asci1 = [ord(c) for c in userName]


                    if s_username==userName:
                        i = studentList.index(stu)
                        break

                if i != -1:

                    quizNum = 0
                    strquiznum = "quiz_" + str(quizNum)

                    for mquiz in studentList[i].getQuizes():
                        if mquiz.getQuizName() == strquiznum:
                            quizNum = quizNum + 1
                            strquiznum = "quiz_" + str(quizNum)

                    quiz.setQuizName(strquiznum)

                    studentList[i].getQuizes().append(quiz)

        self.__oProducer.addIntoExecutionLog("Parsing Quiz file : " + path1 + " finished")


    def quiz(self):
        quiz = pd.read_csv('CSE3063_20201123_Mon_zoom_PollReport.csv')
        quiz.reset_index(inplace=True)
        
        for i in quiz.columns:
            try:
                if quiz[quiz[i].str.contains('Are you attending this lecture?')].shape[0]>0:
                    a = i
            except:
                pass
            
        quiz = quiz[quiz[a]!='Are you attending this lecture?']
        quiz.drop(quiz.columns[0], axis=1, inplace=True)
        
        # Tüm satırı NaN olan kolonları temizle
        for i in quiz.columns[3:]:
            if quiz[quiz[i].isna()].shape[0] == quiz.shape[0]:
                quiz.drop(i, axis=1, inplace=True)
                
                
        # Sütun isimleri
        cols = ['User Name', 'User Mail', 'Submitted Date/Time']
    
        for i in range(int(len(quiz.columns[3:])/2)):
            cols.append('Q'+str(i+1))
            cols.append('A'+str(i+1))
            
        quiz.columns=cols
        
        return quiz

    def parseAnswerKey(self, path2, studentList):

        df_withHeader=pd.read_excel(path2)
        quizName=df_withHeader.columns[0]

        df_answerKey = pd.read_excel(path2, skiprows=1, header=None)
        questionList = df_answerKey.iloc[:, 0]
        answerList = df_answerKey.iloc[:, 1]

        qlist=[]
        alist=[]
        questionList=questionList.values
        answerList=answerList.values

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
                        if studentList[i].getQuizes()[j].getQuizParts()[k].getQuestion().getQuestionText() == self.checkQuestion(qlist[m]):
                            studentList[i].getQuizes()[j].getQuizParts()[k].getQuestion().setAnswer(alist[m])

                            exist=False

                            for mquiz in studentList[i].getQuizes():
                                if mquiz.getQuizName() == quizName:
                                    exist=True

                            if not exist:

                                studentList[i].getQuizes()[j].setQuizName(quizName)
        a=5




    def checkQuestion(self,qText):
        
            if qText.__contains__("\n\r"):
                qText = qText.replace('\n\r', "")


            elif qText.__contains__("\r\n"):
                qText = qText.replace('\r\n', "")

            elif qText.__contains__("\r"):
                qText = qText.replace('\r', "")

            elif qText.__contains__("\t"):
                qText = qText.replace('\t', "")


            elif qText.__contains__("\n"):
                qText = qText.replace('\n', "")



            return qText
            

    """"
    # Sınıf listesini almak için

    class_list = pd.read_excel('studentList.XLS', header=12)
    class_list = class_list[['No', 'Öğrenci No', 'Adı', 'Soyadı', 'Açıklama']]
    class_list = class_list[~class_list['Soyadı'].isna()]
    class_list = class_list[~class_list['Soyadı'].str.contains('Soyadı')]
    class_list.reset_index(drop=True, inplace=True)
    
    class_list = class_list[['No', 'Öğrenci No', 'Adı', 'Soyadı', 'Açıklama']]
    class_list = class_list[~class_list['Soyadı'].isna()]
    class_list = class_list[~class_list['Soyadı'].str.contains('Soyadı')]
    class_list.reset_index(drop=True, inplace=True)
    
    class_list['User Name'] = class_list['Adı'] + ' ' + class_list['Soyadı']
    class_list['User Name'] = class_list['User Name'].str.title()
    """

    """
    # Fonksiyonun, sınıf listesinde adı olup yoklamada adı olmayanları ekleyen hali

    def attendance():
        
        class_list = pd.read_excel('studentList.XLS', header=12)
        class_list = class_list[['No', 'Öğrenci No', 'Adı', 'Soyadı', 'Açıklama']]
        class_list = class_list[~class_list['Soyadı'].isna()]
        class_list = class_list[~class_list['Soyadı'].str.contains('Soyadı')]
        class_list.reset_index(drop=True, inplace=True)
        
        class_list['Adı'] = class_list['Adı'].str.replace('İ', 'i')
        class_list['Adı'] = class_list['Adı'].str.replace('I', 'ı')
        class_list['Adı'] = class_list['Adı'].str.title()
        class_list['Soyadı'] = class_list['Soyadı'].str.replace('İ', 'i')
        class_list['Soyadı'] = class_list['Soyadı'].str.replace('I', 'ı')
        class_list['Soyadı'] = class_list['Soyadı'].str.title()
        
        class_list['User Name'] = class_list['Adı'] + ' ' + class_list['Soyadı']
        
        
        path = input('Input file path: ')
        
        df = pd.read_csv(r'{}'.format(path))
        df.reset_index(inplace=True)
        
        for i in df.columns:
            try:
                if df[df[i].str.contains('Are you attending this lecture?')].shape[0]>0:
                    a = i
    
            except:
                pass
        
        attendance = df[df[a].str.contains('Are you attending this lecture?')]
        attendance = attendance[attendance.columns[1:6]]
        attendance.columns = ['User Name', 'User Mail', 'Submitted Date/Time', 'Q', 'A']
        attendance.rename(columns={'A':attendance['Q'].unique()[0]}, inplace=True)
        attendance.reset_index(drop=True, inplace=True)
        attendance.drop('Q', axis=1, inplace=True)
        attendance['User Name'] = attendance['User Name'].str.title()
        
        date = attendance['Submitted Date/Time'].unique()[0]
        
        attendance = attendance.merge(class_list['User Name'], how='right', on='User Name')
        attendance['Submitted Date/Time'].fillna(date, inplace=True)
        attendance['Are you attending this lecture?'].fillna('No', inplace=True)
        
        return attendance
    """
    """
    # Yukarıdaki örnekte kullanılan dosyaya göre yoklama verisinde Evet diyen öğrenci sayısı:

    df = pd.read_csv('C:/Users/ryilkici/Desktop/CSE3063_20201124_Tue_zoom_PollReport.csv')
    
    df.reset_index(inplace=True)
    
    for i in df.columns:
        try:
            if df[df[i].str.contains('Are you attending this lecture?')].shape[0]>0:
                a = i
    
        except:
            pass
    
    attendance = df[df[a].str.contains('Are you attending this lecture?')]
    attendance = attendance[attendance.columns[1:6]]
    attendance.columns = ['User Name', 'User Mail', 'Submitted Date/Time', 'Q', 'A']
    attendance.rename(columns={'A':attendance['Q'].unique()[0]}, inplace=True)
    attendance.reset_index(drop=True, inplace=True)
    attendance.drop('Q', axis=1, inplace=True)
    attendance['User Name'] = attendance['User Name'].str.title()
    
    attendance[attendance['Are you attending this lecture?']=='Yes'].shape[0]
    """
