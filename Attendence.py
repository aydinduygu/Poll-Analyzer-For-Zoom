import datetime

class Attendence:

    __numStuAttend=None
    __numClasses=None
    __attDates:set=None
    __clsDates:set=None

    def __init__(self):
        self.__numStuAttend=0
        self.__numClasses=0
        self.__attDates={()}
        self.__clsDates={()}

    def add_Attendence(self,date:datetime.date):
        if not date.strftime("%d/%m/%y") in self.__attDates:
            self.__attDates.add(date.strftime("%d/%m/%y"))
            self.__numStuAttend=len(self.__attDates)

    def add_clsDate(self,date:datetime.date):
        if not date.strftime("%d/%m/%y") in self.__clsDates:
            self.__clsDates.add(date.strftime("%d/%m/%y"))
            self.__numClasses = len(self.__clsDates)

    def getNumStuAttend(self):
        return self.__numStuAttend

    def getNumClasses(self):
        return self.__numClasses

    def getAttDates(self):
        return self.__attDates

    def getClsDates(self):
        return self.__clsDates