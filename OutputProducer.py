from datetime import datetime
import pandas as pd

#singleton pattern implemented
class OutputProducer:
    __instance = None

    def __init__(self):
        raise RuntimeError('Call instance() method instead!')

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
        return cls.__instance

    def addIntoExecutionLog(self, logInfo):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        f = open("logFile.txt", "a")
        f.write(dt_string + " " + logInfo + '\n')
        f.close()

        print(dt_string + " " + logInfo + '\n')


    def produceOutput(self,studentList,poll_List):

        global qlist
        attdatalist=[]

        for stu in studentList:
            name=stu.getName().capitalize()
            surname=stu.getSurname().capitalize()
            id=stu.getStudentId()

            if stu.getAttendence==0 and stu.getNumberOfClasses==0:
                attRate=0
            else:
                try:
                    attRate=stu.getAttendence()/stu.getNumberOfClasses()
                except:
                    attRate=0
                    pass

            attPer=attRate*100
            numPoll=len(stu.getQuizes())

            data={"Student Id":id,"Name":name,"Surname":surname,"Attendence":stu.getAttendence(),"Num Classes":stu.getNumberOfClasses(),"Attendance Rate":attRate,"Attendence Percentage":attPer,"Number Of Polls":numPoll}
            attdatalist.append(data)

        df=pd.DataFrame(attdatalist)

        self.addIntoExecutionLog("Attendence report is generated.")

        # i=0
        # for key in poll_List:
        #
        #     stuList=poll_List[key]
        #
        #
        #     for stu in stuList:
        #         name = stu.getName().capitalize()
        #         surname = stu.getSurname().capitalize()
        #         id = stu.getStudentId()
        #         qlist=stu.getQuizes()[i].getQuizParts()
        #         numList = []
        #         for q in qlist:
        #             numList.append(q.getIsCorrect())
        #         print(numList)
        #
        #
        #     i=i+1


        df.to_excel("./attendence_results/attendence_report.xlsx")

