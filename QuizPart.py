from Question import Question
from QuestionStat import QuestionStat
from AnswerStat import  AnswerStat

class QuizPart:
    __question = None
    __studentRespond = None


    def __init__(self, question, studentRespond):
        self.__question = question
        self.__studentRespond = studentRespond
        self.questionStat=QuestionStat()
        self.answerStat=AnswerStat()
        self.__isCorrect=0
        self.answerStat.correctAnswer=question.getAnswer()


    def getQuestion(self):
       return self.__question

    def getStudentRespond(self):
        return self.__studentRespond

    def getIsCorrect(self):
        return self.__isCorrect

    def setIsCorrect(self, value):
        self.__isCorrect=value

    def getQuestionStat(self):
        return self.questionStat

    def getAnswerStat(self):
        return self. answerStat


    def __hash__(self):
        return hash(self.__question)

    def __eq__(self, other):
        if not isinstance(other, QuizPart):
            return False

        if self.getQuestion()== other.getQuestion():

            return True
        else:
            return False

