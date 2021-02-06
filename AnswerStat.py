from collections import OrderedDict

class AnswerStat():


    def __init__(self):

        self.correctAnswer=""
        self.answerNumDict= {}
        self.answerPercDict={}
        self.answerStuDict={}



    def addAnswer(self,answer,stu,numTotalResponders):

        if answer not in self.answerStuDict:
            self.answerStuDict[answer]=[stu]

        else:
            self.answerStuDict[answer].append(stu)

        if answer not in self.answerNumDict:
            self.answerNumDict[answer]=1
        else:
            self.answerNumDict[answer]+=1

            self.answerPercDict[answer]= (100 * self.answerNumDict[answer]) / numTotalResponders



    def setCorrectAnswer(self,answer):
        self.correctAnswer=answer