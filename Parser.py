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

    def attendance(self,path):
       
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

        attendanceList=[]
        
        attendance=attendance['User Name']
        attendanceList.extend(attendance)

        return attendanceList


    """
    # Sınıf listesini almak için

    class_list = pd.read_excel('CES3063_Fall2020_rptSinifListesi.XLS', header=12)
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
        
        class_list = pd.read_excel('CES3063_Fall2020_rptSinifListesi.XLS', header=12)
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