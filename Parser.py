import pandas as pd

from Student import Student
from Quiz import Quiz
from QuizPart import QuizPart
from Question import Question


class Parser:

    def __init__(self):
        pass

    def parseStudentList(self, filePath):
        df = pd.read_excel(filePath, header=12)
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

    def parseAttendance(self, path):

        global a
        df = pd.read_csv(r'{}'.format(path))
        df.reset_index(inplace=True)

        for i in df.columns:
            try:
                if df[df[i].str.contains('Are you attending this lecture?')].shape[0] > 0:
                    a = i

            except:
                pass

        attendance = df[df[a].str.contains('Are you attending this lecture?')]
        attendance = attendance[attendance.columns[1:6]]
        attendance.columns = ['User Name', 'User Mail', 'Submitted Date/Time', 'Q', 'A']
        attendance.rename(columns={'A': attendance['Q'].unique()[0]}, inplace=True)
        attendance.reset_index(drop=True, inplace=True)
        attendance.drop('Q', axis=1, inplace=True)

        attendanceList = []

        attendance = attendance['User Name']
        attendanceList.extend(attendance)

        return attendanceList

    def parseQuiz(self, path1, path2):

        df_quiz = pd.read_csv(path1, skiprows=1, header=None)
        df_answers=pd.read_csv(path2,skiprows=1,header=None)

        numCol = len(df_quiz.columns)
        numRows = len(df_quiz.index)
        q_IndexList = [x for x in range(4, numCol) if x % 2 == 0]
        a_IndexList = [x for x in range(4, numCol) if x % 2 != 0]

        questions = df_quiz[df_quiz.columns[q_IndexList]]
        answers = df_quiz[df_quiz.columns[a_IndexList]]

        qNum = 1

        for x in range(0, numRows):
            for y in range(0, len(q_IndexList)):
                qText = questions[y]
                q = Question(qNum,qText)

        print(len(df_quiz.columns))

    def parseAnswerKey(self, path):
        df = pd.read_excel(path, header=12)
        answerList = self.parseColumn(df, "Answer")
        return answerList

        # mailDf=pd.read_csv(self.__filePath2,usecols="User Email")
        # dataTimeDf=pd.read_csv(self.__filePath2,usecols="Submitted Date/Time")
        # numColumns=len(df.columns)
        #
        # num=df.columns.get_loc("Submitted Date/Time")
        # num=num+1
        #
        # quizDf=df[df.columns[num:numColumns]]
        #
        # mylist=[]
        #
        # mylist.extend(quizDf)
        #
        # print(mylist)

        a = 1


    """
    # QUIZ DATA

    def quiz():
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
    """
    """
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
