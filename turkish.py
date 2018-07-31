import requests
import bs4

class Turkish:
    
    def __init__(self, data):
        self.totalFare = data["totalFare"]
        self.baseFare = data["baseFare"]
        self.taxes = data["taxes"]
        self.dates = data["dates"]
        self.company_codes = data["company_codes"]
        self.currencies = data["currencies"]
        self.rules = data["rules"]

        self.non_ref_fare = 0
    
    def calculate(self):
        rules = self.rules.split("\n")
        beforeDeparture = []
        penalty = []
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
        self.non_ref_fare = self.__get_Exchange_Rates(penalty)
        print(self.non_ref_fare)

        print("\n")
        return None

    def __get_Exchange_Rates(self, data):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        if data[0]=="EUR" or data[0]=="RUB" or data[0]=="USD":
            tenge = html.select('.content_list .'+data[0]+' .price_buy')
            out = tenge[0].getText()
            out = float(out) * float(data[1])
        return out