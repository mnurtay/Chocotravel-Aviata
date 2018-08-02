import bs4

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
        
        self.non_refundable_taxes = 0
        self.sum_fare = 0
        self.check = 0

    def calculate(self):
        
        if self.check == 0:

            if self.__get_status():

                words = self.rules.split("\n")
                print(words)
                
                arr_canc = []
                arr_penalty = []
                non_refundable_taxes = 0
                sum_fare = 0
                refunded_taxes = 0
                check = 0
                ch = 0
                penalty = 0

                for rule in rules:
                    print(rule)
                    if "CHANGES" in rule:
                        check = 1
                    elif "CANCELLATIONS" in rule:
                        check = 2
                    if check == 2:
                        arr_canc.append(rule)
        
                for rule in arr_canc:
                    if "BEFORE DEPARTURE" in rule:
                        ch = 1

                    elif "AFTER DEPARTURE" in rule:
                        ch = 2

                    if ch == 1 and "CHARGE RUB" in rule:
                        pen = rule.split()[2]
                        arr_penalty.append(pen)
                        break

                penalty = round(self.__get_Exchange_Rates(arr_penalty), 1)

                self.sum_fare = self.baseFare - penalty
                self.total = self.totalFare - penalty - self.non_refundable_taxes

                output = {}
                output['non_refundable_taxes'] = self.non_refundable_taxes
                output['penalty'] = penalty
                output['refunded_fare'] = self.sum_fare
                output['refunded_taxes'] = self.totalTaxes
                output['refunded_total'] =self.total
                output['name'] = self.name
                output['currency']: self.currencies

                return output
            return 'Error'
        return 'Error'

    def __get_status(self):
        return self.now < self.depDate

    def __get_Exchange_Rates(self, data):
        site = requests.get('https://prodengi.kz/currency/')
        html = bs4.BeautifulSoup(site.text, "html.parser")
        if data[0]=="EUR" or data[0]=="RUB" or data[0]=="USD":
            tenge = html.select('.content_list .'+data[0]+' .price_buy')
            out = tenge[0].getText()
            out = float(out) * float(data[1])
        return out