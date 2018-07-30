import requests
import bs4

class Aeroflot:
    
    def __init__(self, data):
        self.totalFare = int(data['totalFare'])
        self.baseFare = int(data['baseFare'])
        self.rules = data['rules']
        self.taxes = data['taxes']
        self.dates = data['dates']
        self.ch = 0
        self.changeRules = []
        self.ofNoShow = True


    # Ваш тариф: Эконом Бюджет
    def calculate(self):
        print("Total fare is",self.totalFare)
        print("Base fare is",self.baseFare)
        print("Taxes: ",(self.totalFare-self.baseFare),"\n",self.taxes)
        print("Departure Date:",self.dates[1],"\n")

        rules = self.rules.split("\n")
        notReturnValue = None
        for rule in rules:
            if "CHANGES" in rule:
                self.ch = 1
            elif "CANCELLATION" in rule:
                self.ch = 2
            if self.ch == 1:
                self.changeRules.append(rule)
        
        self.__check_ofNoShow()
        if not self.ofNoShow and not self.__get_status():
            return 0

        for rule in self.changeRules:
            if "REISSUE/REVALIDATION" in rule:
                temp = rule.split()
                notReturnValue = self.__get_Exchange_Rates(temp[1], float(temp[2]))
            if "TAX" in rule:
                print(rule)
        return self.baseFare - notReturnValue
    
    def __get_Exchange_Rates(self, course, amount):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        price = None
        if course=="EUR" or course=="RUB" or course=="USD":
            tenge = html.select('.content_list .'+course+' .price_buy')
            price = tenge[0].getText()
            price = float(price) * float(amount)
        return price
    
    def __get_status(self):
        return self.dates[0] < self.dates[1]

    def __check_ofNoShow(self):
        for rule in self.changeRules:
            if "NOT PERMITTED" in rule and "NO-SHOW" in rule:
                self.ofNoShow = False
                break
                
        
