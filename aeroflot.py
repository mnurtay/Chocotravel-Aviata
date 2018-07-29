class Aeroflot:
    
    def __init__(self, totalFare, baseFare, rules, taxes, dates):
        self.totalFare = totalFare
        self.baseFare = baseFare
        self.rules = rules
        self.taxes = taxes
        self.dates = dates
        self.ch = 0


    # Ваш тариф: Эконом Бюджет
    def calculate(self):
        return self.__set_coef()

    def __set_coef(self):
        rules = self.rules.split("\n")
        for rule in rules:
            if 'CANCELLATION' in rule:
                self.ch = 1
            elif self.ch == 1 and 'CHANGES' in rule:
                
        print("Ещё не доработан")
