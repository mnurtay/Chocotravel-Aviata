import datetime

class Status:
    departureDate = ""
    currentDate = ""

    def __init__(self, departureDate):
        self.departureDate = departureDate
        self.currentDate = datetime.datetime.now().isoformat()

    def get(self):
        self.__split()
        departureDate = self.__castDate(self.departureDate)
        currentDate = self.__castDate(self.currentDate)
        return currentDate < departureDate

    def __split(self):
        self.departureDate = self.departureDate.split("T", 1)
        self.currentDate = self.currentDate.split("T", 1)
        self.currentDate[1] = self.currentDate[1].split(".", 1)[0]
    
    def __castDate(self, data):
        date = data[0].split("-", 2)
        time = data[1].split(":", 2)
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 
                int(time[0]), int(time[1]), int(time[2]))
        return date
