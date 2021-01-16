from datetime import datetime


class OutputProducer:

    def __init__(self):
        pass

    def addIntoExecutionLog(self, logInfo):

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        f = open("logFile.txt", "a")
        f.write(dt_string + " " + logInfo + '\n')
        f.close()

        print(dt_string + " " + logInfo + '\n')
