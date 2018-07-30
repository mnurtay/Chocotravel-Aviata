import requests
import bs4

class Aeroflot:
    
    def __init__(self, data):
        self.totalFare = int(data['totalFare'])
        self.baseFare = int(data['baseFare'])
        self.rules = data['rules']
        self.taxes = data['taxes']
        self.sumTaxes = self.totalFare - self.baseFare
        self.dates = data['dates']
        self.ch = 0
        self.changeRules = []
        self.cancelRulue = []
        self.ofNoShow = True

    def calculate(self):
        print("Total fare is",self.totalFare)
        print("Base fare is",self.baseFare)
        print("Taxes: ",(self.totalFare-self.baseFare),"\nTypes:")
        for tax in self.taxes:
            print("   ", tax[0], "=",tax[1])
        print("Departure Date:",self.dates[1],"\n")

        rules = self.rules.split("\n")
        notReturnValue = []
        for rule in rules:
            if "CHANGES" in rule:
                self.ch = 1
            elif "CANCELLATION" in rule:
                self.ch = 2
            if self.ch == 1:
                self.changeRules.append(rule)
            else:
                self.cancelRulue.append(rule)
        
        self.__check_ofNoShow()
        if not self.ofNoShow and not self.__get_status():
            return 0

        for rule in self.changeRules:
            if "REISSUE/REVALIDATION" in rule:
                temp = rule.split()
                notReturnValue.append(rule)
                notReturnValue.append(self.__get_Exchange_Rates(temp[1], float(temp[2])))
                break
            if "TAX" in rule:
                print(rule)
        notReturnValue[1] = (self.baseFare-notReturnValue[1])+self.sumTaxes
        return notReturnValue
    
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
                
        
