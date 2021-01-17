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


    def produceOutput(self,studentList):

        df=pd.DataFrame(studentList)
        print(df)
