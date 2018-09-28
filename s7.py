import bs4
import requests

class S7:
    
    def __init__(self, data):
        self.totalFare = int(data['totalFare'])     
        self.baseFare = int(data['baseFare'])
        self.rules = data['rules']                  
        self.taxes = data['taxes']                  
        self.now = data['dates'][0]                 
        self.depDate = data['dates'][1]
        self.totalTaxes = self.totalFare-self.baseFare
        self.company_codes = data['company_codes']
        self.currencies = data['currencies']
        self.name = 'S7 Airlines'
        
        self.status = " "
        self.non_refundable_taxes = 0
        self.sum_fare = 0
        self.non_ref = []
        self.check = 0
        self.bool = None

    def calculate(self):
        #print(self.check)

        if self.check == 0:

            words = self.rules.split("\n")
            #print(words)
                
            arr_canc = []
            arr_penalty = []
            non_refundable_taxes = 0
            sum_fare = 0
            refunded_taxes = 0
            check = 0
            #ch = 0
            #penalty = 0

            for rule in words:
                #print(rule)
                if "CHANGES" in rule:
                    check = 1 
                elif "CANCELLATIONS" in rule:
                    check = 2

                if check == 2:
                    arr_canc.append(rule)

                
            for rule in arr_canc:
                #print(rule)
                if self.status == "CANCEL" or self.status == "NO-SHOW" or self.status == "REFUND":
                    if not self.now < self.depDate:
                        return None

                if check == 2:
                    if "CANCEL/NO-SHOW/REFUND" in rule:
                        if "NON_REFUNDABLE" in rule:
                            self.bool = False
                            break

                    elif "CHARGE EUR" or "CHARGE RUB" or "CHARGE USD" in rule:
                        for i in rule.split():
                            if i == "EUR" or i == "RUB" or i == "USD":
                                arr_penalty.append(i)

            non_ref = 0

            if self.bool:
                non_ref = round(self.__get_Exchange_Rates(arr_penalty), 1)
            else:
                non_ref = self.baseFare

            #print(self.non_refundable_taxes)
            # print(penalty)
            # print(self.sum_fare)
            # print(self.totalTaxes)
            # print(self.total)
            # print(self.name)
            # print(self.currencies)

            output = {}

            if self.bool:
                output['non_refundable taxes'] = self.totalTaxes
                output['penalty'] = str(non_ref)
                output['refunded_fare'] = self.baseFare - non_ref
                output['refunded_taxes'] = 0
                output['refunded_total'] = (self.baseFare-non_ref_fare) + refunded_taxes
                output['name'] = self.name
                output['currency']= self.currencies
            else:
                output['non_refundable taxes'] = self.totalTaxes
                output['penalty'] = str(self.baseFare)
                output['refunded_fare'] = self.baseFare - non_ref
                output['refunded_taxes'] = 0
                output['refunded_total'] = 0
                output['name'] = self.name
                output['currency']= self.currencies

            return output

        return 'Error'

    def __get_Exchange_Rates(self, data):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        if data[0]=="EUR" or data[0]=="RUB" or data[0]=="USD":
            tenge = html.select('.content_list .'+data[0]+' .price_buy')
            out = tenge[0].getText()
            out = float(out) * float(data[1])
        return out