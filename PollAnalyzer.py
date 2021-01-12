from Student import Student
import pandas as pd
from Parser import Parser


class PollAnalyzer:



        filePath1 = "CES3063_Fall2020_rptSinifListesi.XLS"
        filePath2 = "CSE3063_20201123_Mon_zoom_PollReport.csv"
        parser = Parser(filePath1, filePath2)

        parser.parsestudentlist()


