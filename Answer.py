class Answer():


    def __init__(self):
        self.answerText=""
        self.isCorrect=None
        self.studentsUsed=[]
        self.numStudentsUsed=0


    def setAnswerText(self,answerText):
        self.answerText=answerText


    def setIsCorrect(self,value):
        self.isCorrect=value

    def addStudent(self,stu):

        self.studentsUsed.append(stu)
        self.numStudentsUsed+=1

