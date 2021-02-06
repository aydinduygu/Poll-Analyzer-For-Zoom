from AnswerStat import AnswerStat

class QuestionStat():

    def __init__(self):

        self.question=None
        self.answerStat=AnswerStat()
        self.correctResponders=[]
        self.wrongResponders=[]
        self.numCorrectResponders=0
        self.numWrongResponders=0
        self.correctRespPerc=0
        self.wrongRespPerc=0
        self.numTotalResponders=0

    def setQuestion(self,question):
        self.question=question

    def getAnswerStat(self):
        return self.answerStat

    def addCorrectResp(self,stu):
        self.correctResponders.append(stu)
        self.numCorrectResponders+=1
        self.numTotalResponders+=1
        self.updatePercentages()

    def addWrongResp(self,stu):
        self.wrongResponders .append(stu)
        self.numWrongResponders+=1
        self.numTotalResponders += 1
        self.updatePercentages()

    def updatePercentages(self):

        self.correctRespPerc=100*self.numCorrectResponders/self.numTotalResponders
        self.wrongRespPerc=100*self.numWrongResponders/self.numTotalResponders