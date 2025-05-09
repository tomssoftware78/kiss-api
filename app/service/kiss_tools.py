from datetime import date, datetime, timedelta

class KissTools:
    def __init__(self):
        raise NotImplementedError("This is a utility class and cannot be instantiated.")

    @staticmethod
    def convertKissDetailToCaseID(detail):
        return (int)(re.sub(r'[^0-9]', '', detail)[:-3])

    @staticmethod
    def convertKissDetailToCaseName(detail):
        return detail.removeprefix("RCCU/")[:-4]

    @staticmethod
    def convertCaseIDToKissDetail(id):
        caseId = ((str)(id))
        caseId = "RCCU/" + caseId[0:2]+"/" + caseId[2:6] + "/"
        return caseId