import string
from TR_Text import tr_upper,tr_lower
import locale

# -*- coding: utf-8 -*-

class StringComparator:
    s1 = None
    s2 = None

    s1_list=None
    s2_list=None

    s1_lower = None
    s1_upper = None

    s1_C_S_P_N=None
    s1_noSpace = None
    s1_noPunc = None
    s1_noPuncNoSpace=None
    s1_lowerNoSpace = None
    s1_upperNoSpace = None
    s1_lowerNoPunc = None
    s1_upperNoPunc = None
    s1_lowerNoNumNoPunc=None
    s1_lowerNoSpaceNoPunc = None
    s1_upperNoSpaceNoPunc = None

    s2_C_S_P_N=None
    s2_lower = None
    s2_upper = None
    s2_noSpace = None
    s2_noPunc = None
    s2_noPuncNoSpace = None
    s2_lowerNoSpace = None
    s2_upperNoSpace = None
    s2_lowerNoPunc = None
    s2_upperNoPunc = None
    s2_lowerNoNumNoPunc = None
    s2_lowerNoSpaceNoPunc = None
    s2_upperNoSpaceNoPunc = None

    cmp_=None
    cmp_ig_CaseNumBlock=None
    cmp_ig_Case = None
    cmp_ig_Punc = None
    cmp_ig_Space = None
    cmp_ig_CasePunc = None
    cmp_ig_CaseSpace = None
    cmp_ig_SpacePunc = None
    cmp_ig_CaseSpacePunc = None
    cmp_ig_C_S_P_N=None
    cmp_w_by_w=None
    cmp_w_by_w_NoNum=None


    def __init__(self, string1: str, string2: str):

        locale.setlocale(locale.LC_COLLATE,"tr_TR.utf8")

        if string1 == None:
            raise RuntimeError("String1 is Null!")
        if string2 == None:
            raise RuntimeError("String2 is Null")

        if string1 != None and string2 != None:

            self.cmp_=(string1==string2)

            self.s1 = string1
            self.s2 = string2
            self.__comp_ig_Case()
            self.__comp_ig_Punc()
            self.__comp_ig_Space()
            self.__comp_ig_CasePunc()
            self.__comp_ig_CaseSpace()
            self.__comp_ig_SpacePunc()
            self.__comp_ig_CaseSpacePunc()
            self.__comp_ig_C_S_P_N()
            self._comp_wordByWord()
            self._comp_wordByWord_noNum()


    def __comp_ig_Case(self):

        self.s1_lower=tr_lower(self.s1)
        self.s2_lower = tr_lower(self.s2)

        self.s1_upper=tr_upper(self.s1)
        self.s2_upper=tr_upper(self.s2)

        self.cmp_ig_Case=self.compare(self.s1_lower,self.s2_lower)


    def __comp_ig_Punc(self):


        s1 = self.s1
        s2 = self.s2
        self.s1_noPunc = s1.translate(str.maketrans('', '', string.punctuation))
        self.s2_noPunc = s2.translate(str.maketrans('', '', string.punctuation))

        esList = ['\n', '\t', '\r']
        for es in esList:
            if es in self.s1_noPunc:
                self.s1_noPunc.replace(es,' ')
            if es in self.s2_noPunc:
                self.s2_noPunc.replace(es,' ')

        self.cmp_ig_Punc = self.compare(self.s1_noPunc,self.s2_noPunc)

    def __comp_ig_Space(self):
        s1 = self.s1
        s2 = self.s2

        self.s1_noSpace = s1.replace(' ', '')
        self.s2_noSpace = s2.replace(' ', '')
        self.cmp_ig_Space = self.compare(self.s1_noSpace,self.s2_noSpace)

    def __comp_ig_CasePunc(self):

        self.s1_lowerNoPunc = self.s1_lower.translate(str.maketrans('', '', string.punctuation))
        self.s2_lowerNoPunc = self.s2_lower.translate(str.maketrans('', '', string.punctuation))
        self.s1_upperNoPunc = self.s1_upper.translate(str.maketrans('', '', string.punctuation))
        self.s2_upperNoPunc = self.s2_upper.translate(str.maketrans('', '', string.punctuation))

        esList = ['\n', '\t', '\r']
        for es in esList:
            if es in self.s1_lowerNoPunc:
                self.s1_lowerNoPunc.replace(es, ' ')
            if es in self.s2_lowerNoPunc:
                self.s2_lowerNoPunc.replace(es, ' ')

        for es in esList:
            if es in self.s1_upperNoPunc:
                self.s1_upperNoPunc.replace(es, ' ')
            if es in self.s2_upperNoPunc:
                self.s2_upperNoPunc.replace(es, ' ')
        self.cmp_ig_CasePunc = self.compare(self.s1_lowerNoPunc, self.s2_lowerNoPunc)

    def __comp_ig_CaseSpace(self):

        self.s1_lowerNoSpace = self.s1_lower.replace(" ", "")
        self.s2_lowerNoSpace = self.s2_lower.replace(" ", "")
        self.s1_upperNoSpace = self.s1_upper.replace(" ", "")
        self.s2_upperNoSpace = self.s2_upper.replace(" ", "")

        self.cmp_ig_CaseSpace = self.compare(self.s1_lowerNoSpace, self.s2_lowerNoSpace)

    def __comp_ig_SpacePunc(self):


        self.s1_noPuncNoSpace = self.s1_noPunc.replace(" ", "")
        self.s2_noPuncNoSpace = self.s2_noPunc.replace(" ", "")
        self.cmp_ig_SpacePunc=self.compare(self.s1_noPuncNoSpace,self.s2_noPuncNoSpace)


    def __comp_ig_CaseSpacePunc(self):

        self.s1_lowerNoSpaceNoPunc = self.s1_lowerNoPunc.replace(" ", "")
        self.s2_lowerNoSpaceNoPunc = self.s2_lowerNoPunc.replace(" ", "")
        self.s1_upperNoSpaceNoPunc = self.s1_upperNoPunc.replace(" ", "")
        self.s2_upperNoSpaceNoPunc = self.s2_upperNoPunc.replace(" ", "")
        self.cmp_ig_CaseSpacePunc = self.compare(self.s1_lowerNoSpaceNoPunc, self.s2_lowerNoSpaceNoPunc)

    def __comp_ig_C_S_P_N(self):

        self.s1_C_S_P_N=""
        self.s2_C_S_P_N = ""

        for s in self.s1_lowerNoSpaceNoPunc:
            if not s.isdigit():
                self.s1_C_S_P_N+=s

        for s in self.s2_lowerNoSpaceNoPunc:
            if not s.isdigit():
                self.s2_C_S_P_N+=s


        case1=self.s1_lowerNoSpaceNoPunc.__contains__(self.s2_C_S_P_N)
        case2=self.s2_lowerNoSpaceNoPunc.__contains__(self.s1_C_S_P_N)
        case3=self.s1_lowerNoSpaceNoPunc==self.s2_C_S_P_N
        if (case1 or case2 or case3):
            self.cmp_ig_C_S_P_N =0
        else:
            self.cmp_ig_C_S_P_N=self.compare(self.s1_C_S_P_N,self.s2_C_S_P_N)

    def _comp_wordByWord(self):

        s1_list=self.s1_lowerNoPunc.split()
        s2_list=self.s2_lowerNoPunc.split()

        s1_list = [x.strip() for x in s1_list]
        s2_list = [x.strip() for x in s2_list]

        for s in range(min(len(s1_list), len(s2_list))):

            if s1_list[s] != s2_list[s]:

                self.cmp_w_by_w_NoNum = self.compare(s1_list[s], s2_list[s])
                if self.cmp_w_by_w != 0:
                    break
            else:
                self.cmp_w_by_w = 0

        if self.cmp_w_by_w_NoNum == 0:
            if len(s1_list) > len(s2_list):
                self.cmp_w_by_w_NoNum = 1
            elif len(s1_list) < len(s2_list):
                self.cmp_w_by_w_NoNum = -1



    def _comp_wordByWord_noNum(self):


        self.s1_lowerNoNumNoPunc = ""
        self.s2_lowerNoNumNoPunc = ""

        for s in self.s1_lowerNoPunc:
            if not s.isdigit():
                self.s1_lowerNoNumNoPunc += s

        for s in self.s2_lowerNoPunc:
            if not s.isdigit():
                self.s2_lowerNoNumNoPunc += s

        s1_listNoNum =self.s1_lowerNoNumNoPunc.split()
        s2_listNoNum=self.s2_lowerNoNumNoPunc.split()

        s1_listNoNum=[x.strip() for x in s1_listNoNum]
        s2_listNoNum = [x.strip() for x in s2_listNoNum]


        for s in range(min(len(s1_listNoNum),len(s2_listNoNum))):

            if s1_listNoNum[s]!=s2_listNoNum[s]:

               self.cmp_w_by_w_NoNum = self.compare(s1_listNoNum[s],s2_listNoNum[s])
               if self.cmp_w_by_w_NoNum!=0:
                   break
            else:
                self.cmp_w_by_w_NoNum =0

        if self.cmp_w_by_w_NoNum==0:
            if len (s1_listNoNum)>len(s2_listNoNum):
                self.cmp_w_by_w_NoNum=1
            elif len (s1_listNoNum)<len(s2_listNoNum):
                self.cmp_w_by_w_NoNum = -1




    def compare(self,s1,s2):
        if locale.strxfrm(s1)>locale.strxfrm(s2):
            return 1
        elif locale.strxfrm(s1)<locale.strxfrm(s2):
            return -1
        else:
            return 0