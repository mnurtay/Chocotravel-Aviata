import requests
import bs4

class Aeroflot:
    
    def __init__(self, data):
        self.totalFare = int(data['totalFare'])
        self.baseFare = int(data['baseFare'])
        self.rules = data['rules']
        self.taxes = data['taxes']
        self.non_ref_taxes = None
        self.sumTaxes = self.totalFare - self.baseFare
        self.dates = data['dates']
        self.currency = data['currencies']
        self.changeRules = []
        self.cancelRulue = []

    def calculate(self):
        self.__split_rules()
        
        penaltyStr = None
        penaltyValue = None        
        
        if not self.__check_ofNoShow() and not self.__get_status():
            return None
        
        for rule in self.changeRules:
            if "REISSUE/REVALIDATION" in rule:
                temp = rule.split()
                penaltyStr = temp[2]+temp[1]
                penaltyValue = self.__get_Exchange_Rates(temp[1], float(temp[2]))
                break

        self.non_ref_taxes = self.__non_refundable_taxes()
        refunded_taxes = 0
        non_refunded_taxes = 0
        for tax in self.taxes:
            if not tax["Type"] in self.non_ref_taxes:
                refunded_taxes += int(tax["Amount"])
            else:
                non_refunded_taxes += int(tax["Amount"])

        output = {
            'total taxes': self.sumTaxes,
            'non_refundable taxes': non_refunded_taxes,
            'penalty': penaltyStr+" or "+str(int(penaltyValue))+"KZT",
            'refunded_fare': self.baseFare - penaltyValue,
            'refunded_taxes':  refunded_taxes,
            'refunded_total': (self.baseFare-penaltyValue)+refunded_taxes,
            'name': "Aeroflot",
            'currency': self.currency
        }

        return output
    
    def __split_rules(self):
        rules = self.rules.split("\n")
        ch = 0
        for rl in rules:
            if "CHANGES" in rl:
                ch = 1
            elif "CANCELLATION" in rl:
                ch = 2
            if ch == 1:
                self.changeRules.append(rl)
            else:
                self.cancelRulue.append(rl)
            
    def __non_refundable_taxes(self):
        rules = self.rules.split("\n")
        non_ref = None
        for rule in rules:
            if "IN THIS CASE" in rule:
                non_ref = rule.split()[6].split("/")
                break
        return non_ref

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
                return False

                
        
