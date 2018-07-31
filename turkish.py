import requests
import bs4

class Turkish:
    
    def __init__(self, data):
        self.totalFare = data["totalFare"]
        self.baseFare = data["baseFare"]
        self.totalTaxes = self.totalFare-self.baseFare
        self.taxes = data["taxes"]
        self.dates = data["dates"]
        self.company_codes = data["company_codes"]
        self.currencies = data["currencies"]
        self.rules = data["rules"]
    
    def calculate(self):
        if not self.dates[0] < self.dates[1]:
            return None
        rules = self.rules.split("\n")
        beforeDeparture = []
        penalty = []
        non_refunded_taxes = 0
        refunded_taxes = 0
        check = 0
        for rule in rules:
            if "REISSUE/REVALIDATION" in rule:
                penalty.append(rule.split()[1])
                penalty.append(float(rule.split()[2]))
            if "A-BEFORE DEPARTURE" in rule:
                check = 1
            elif "AFTER DEPARTURE" in rule:
                check = 2
            if check == 1:
                beforeDeparture.append(rule)
        non_ref_fare = round(self.__get_Exchange_Rates(penalty), 1)
        if non_refunded_taxes == 0:
            refunded_taxes = self.totalTaxes
        print("\n")
        output = {
            'total taxes': self.totalTaxes,
            'non_refundable taxes': non_refunded_taxes,
            'penalty': str(penalty[1])+penalty[0]+" or "+str(non_ref_fare)+"KZT",
            'refunded_fare': self.baseFare - non_ref_fare,
            'refunded_taxes':  refunded_taxes,
            'refunded_total': (self.baseFare-non_ref_fare)+refunded_taxes,
            'name': "Turkish AirLine",
            'currency': self.currencies
        }
        return output

    def __get_Exchange_Rates(self, data):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        if data[0]=="EUR" or data[0]=="RUB" or data[0]=="USD":
            tenge = html.select('.content_list .'+data[0]+' .price_buy')
            out = tenge[0].getText()
            out = float(out) * float(data[1])
        return out