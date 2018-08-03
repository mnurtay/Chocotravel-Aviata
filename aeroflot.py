import requests
import bs4

class Aeroflot:
    
    def __init__(self, data):
        self.totalFare = int(data['totalFare'])
        self.baseFare = int(data['baseFare'])
        self.rules = data['rules']
        self.taxes = data['taxes']
        self.dates = data['dates']
        self.currency = data['currencies']
        self.cancelRule = []

    def calculate(self):
        self.__split_rules()
        penalty = []
        check = None  
        
        for rule in self.cancelRule:
            if "CANCEL/NO-SHOW/" in rule:
                if "IS NON-REFUNDABLE" in rule:
                    check = False
                    penalty.append(self.baseFare)
                    break
                temp = rule.split()
                penalty[1] = temp[2]+temp[1]
                penalty[0] = round(self.__get_Exchange_Rates(temp[1], float(temp[2])), 1)
                break
        
        non_refunded_taxes = self.totalFare-self.baseFare
        refunded_taxes = 0
        if check:
            non_ref_taxes = self.__non_refundable_taxes()
            non_refunded_taxes = 0
            for tax in self.taxes:
                if not tax["Type"] in self.non_ref_taxes:
                    refunded_taxes += int(tax["Amount"])
                else:
                    non_refunded_taxes += int(tax["Amount"])

        output = {
            'name': "Aeroflot",
            'currency': self.currency,
            'non_refundable taxes': non_refunded_taxes,
            'refunded_taxes': refunded_taxes,
            'refunded_fare': self.baseFare - int(penalty[0])
        }
        if check:
            output['penalty'] = str(penalty[1])+" "+penalty[0]+" or "+str(non_ref_fare)+" "+"KZT"
            output['refunded_total'] = (self.baseFare-non_ref_fare)+refunded_taxes
        else:
            output['penalty'] = str(self.baseFare)+" "+"KZT"  
            output['refunded_total'] = 0

        return output
    
    def __split_rules(self):
        rules = self.rules.split("\n")
        ch = 0
        for rule in rules:
            if "CHANGES" in rule:
                ch = 1
            elif "CANCELLATION" in rule:
                ch = 2
            if ch == 2:
                self.cancelRule.append(rule)
            
    def __non_refundable_taxes(self):
        non_ref = None
        for rule in self.cancelRule:
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