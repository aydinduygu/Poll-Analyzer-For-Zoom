import string


class StringComparator:
    s1 = None
    s2 = None

    s1_lower = None
    s1_upper = None
    s1_noSpace = None
    s1_noPunc = None
    s1_noPuncNoSpace=None
    s1_lowerNoSpace = None
    s1_upperNoSpace = None
    s1_lowerNoPunc = None
    s1_upperNoPunc = None
    s1_lowerNoSpaceNoPunc = None
    s1_upperNoSpaceNoPunc = None

    s2_lower = None
    s2_upper = None
    s2_noSpace = None
    s2_noPunc = None
    s2_noPuncNoSpace = None
    s2_lowerNoSpace = None
    s2_upperNoSpace = None
    s2_lowerNoPunc = None
    s2_upperNoPunc = None
    s2_lowerNoSpaceNoPunc = None
    s2_upperNoSpaceNoPunc = None

    cmp_ig_Case = None
    cmp_ig_Punc = None
    cmp_ig_Space = None
    cmp_ig_CasePunc = None
    cmp_ig_CaseSpace = None
    cmp_ig_SpacePunc = None
    cmp_ig_CaseSpacePunc = None

    def __init__(self, string1: str, string2: str):

        if string1 == None:
            raise RuntimeError("String1 is Null!")
        if string2 == None:
            raise RuntimeError("String2 is Null")

        if string1 != None and string2 != None:
            self.s1 = string1
            self.s2 = string2
            self.__comp_ig_Case()
            self.__comp_ig_Punc()
            self.__comp_ig_Space()
            self.__comp_ig_CasePunc()
            self.__comp_ig_CaseSpace()
            self.__comp_ig_SpacePunc()
            self.__comp_ig_CaseSpacePunc()


    def __comp_ig_Case(self):

        s1 = self.s1
        s2 = self.s2

        turUpper = ['İ', 'I', 'Ü', 'Ç', 'Ş', 'Ğ', 'Ş', 'Ç', 'Ö']
        turLower = ['i', 'ı', 'ü', 'ç', 's', 'ğ', 'ş', 'ç', 'ö']
        for s in range(len(turUpper)):
            if s1.__contains__(turUpper[s]):
                s1.replace(turUpper[s], turLower[s])
            if s2.__contains__(turUpper[s]):
                s2.replace(turUpper[s], turLower[s])

        self.s1_lower = s1.lower()
        self.s2_lower = s2.lower()

        s1 = self.s1
        s2 = self.s2

        for s in range(len(turLower)):
            if s1.__contains__(turLower[s]):
                s1.replace(turLower[s], turUpper[s])
            if s2.__contains__(turLower[s]):
                s2.replace(turLower[s], turUpper[s])

        self.s1_upper = s1.upper()
        self.s2_upper = s2.upper()
        self.cmp_ig_Case = (self.s1_lower == self.s2_lower)

    def __comp_ig_Punc(self):

        s1 = self.s1
        s2 = self.s2
        self.s1_noPunc = s1.translate(str.maketrans('', '', string.punctuation))
        self.s2_noPunc = s2.translate(str.maketrans('', '', string.punctuation))
        self.cmp_ig_Punc = (self.s1_noPunc == self.s2_noPunc)

    def __comp_ig_Space(self):
        s1 = self.s1
        s2 = self.s2

        self.s1_noSpace = s1.replace(' ', '')
        self.s2_noSpace = s2.replace(' ', '')
        self.cmp_ig_Space = (self.s1_noSpace == self.s2_noSpace)

    def __comp_ig_CasePunc(self):

        self.s1_lowerNoPunc = self.s1_lower.translate(str.maketrans('', '', string.punctuation))
        self.s2_lowerNoPunc = self.s2_lower.translate(str.maketrans('', '', string.punctuation))
        self.s1_upperNoPunc = self.s1_upper.translate(str.maketrans('', '', string.punctuation))
        self.s1_upperNoPunc = self.s1_upper.translate(str.maketrans('', '', string.punctuation))
        self.cmp_ig_CasePunc = (self.s1_lowerNoPunc == self.s2_lowerNoPunc)

    def __comp_ig_CaseSpace(self):

        self.s1_lowerNoSpace = self.s1_lower.replace(" ", "")
        self.s2_lowerNoSpace = self.s2_lower.replace(" ", "")
        self.s1_upperNoSpace = self.s1_upper.replace(" ", "")
        self.s2_upperNoSpace = self.s2_upper.replace(" ", "")

        self.cmp_ig_CaseSpace = (self.s1_lowerNoSpace == self.s2_lowerNoSpace)

    def __comp_ig_SpacePunc(self):

        self.s1_noPuncNoSpace = self.s1_noPunc.replace(" ", "")
        self.s2_noPuncNoSpace = self.s2_noPunc.replace(" ", "")

    def __comp_ig_CaseSpacePunc(self):

        self.s1_lowerNoSpaceNoPunc = self.s1_upperNoPunc.replace(" ", "")
        self.s2_lowerNoSpaceNoPunc = self.s2_upperNoPunc.replace(" ", "")
        self.s1_upperNoSpaceNoPunc = self.s1_upperNoPunc.replace(" ", "")
        self.s2_upperNoSpaceNoPunc = self.s2_upperNoPunc.replace(" ", "")
        self.cmp_ig_SpacePunc = (self.s1_lowerNoSpaceNoPunc == self.s2_lowerNoSpaceNoPunc)

