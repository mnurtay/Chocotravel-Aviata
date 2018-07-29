import requests
import bs4

class Aeroflot:
    
    def __init__(self, totalFare, baseFare, rules, taxes, dates):
        self.totalFare = totalFare
        self.baseFare = baseFare
        self.rules = rules
        self.taxes = taxes
        self.dates = dates
        self.ch = 0
        self.changeRules = []


    # Ваш тариф: Эконом Бюджет
    def calculate(self):
        return self.__set_coef()

    def __set_coef(self):
        rules = self.rules.split("\n")
        for rule in rules:
            if "CHANGES" in rule:
                self.ch = 1
            elif "CANCELLATION" in rule:
                self.ch = 2
            if self.ch == 1:
                self.changeRules.append(rule)
        
        for rule in self.changeRules:
            pass
        return self.__get_Exchange_Rates("EUR")
    
    def __get_Exchange_Rates(self, course):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        tenge = html.select('.content_list .'+course+' .price_buy')
        price = tenge[0].getText()
        return price
    

                
        
