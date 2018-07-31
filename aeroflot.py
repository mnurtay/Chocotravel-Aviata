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
        #self.currency = data['currency']
        self.currency = "KZT"
        self.changeRules = []
        self.cancelRulue = []

    def calculate(self):
        print("Total fare is",self.totalFare)
        print("Base fare is",self.baseFare)
        print("Taxes: ",(self.totalFare-self.baseFare),"\nTypes:")
        ch = 0
        for tax in self.taxes:
            print("   ", tax[0], "=",tax[1])
        print("Departure Date:",self.dates[1],"\n")
        rules = self.rules.split("\n")

        penaltyStr = None
        penaltyValue = None

        for rule in rules:
            if "CHANGES" in rule:
                ch = 1
            elif "CANCELLATION" in rule:
                ch = 2
            if ch == 1:
                self.changeRules.append(rule)
            else:
                self.cancelRulue.append(rule)
        
        if not self.__check_ofNoShow() and not self.__get_status():
            return 0

        for rule in self.changeRules:
            if "REISSUE/REVALIDATION" in rule:
                temp = rule.split()
                penaltyStr = temp[2]+temp[1]
                penaltyValue = self.__get_Exchange_Rates(temp[1], float(temp[2]))
                break

        self.non_ref_taxes = self.__non_refundable_taxes()
        refunded_taxes = []
        sum_refunded_taxes = 0
        for tax in self.taxes:
            if not tax[0] in self.non_ref_taxes:
                refunded_taxes.append(tax)
                sum_refunded_taxes += int(tax[1])

        output = {
            'non_refundable taxes': self.non_ref_taxes,
            'penalty': penaltyStr+" or "+str(int(penaltyValue))+"KZT",
            'refunded_fare': self.baseFare - penaltyValue,
            'refunded_taxes':  refunded_taxes,
            'refunded_total': sum_refunded_taxes,
            'operating_company': "Aeroflot",
            'currency': self.currency
        }

        return output
    
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

                
        
