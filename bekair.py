import xml.dom.minidom

class BekAir():
    
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
		self.name = 'Bek Air'	

		#self.mode = ' '
		self.check = 0  
		#self.arr_rules = []
		self.before = 0
		self.non_refundable_taxes = 0
		self.sum_fare = 0

	def calculate(self):

		if self.before == 0:

			if self.__get_status():

				# print('Total fare: ' + str(self.totalFare))
				# print('Base fare: ' + str(self.baseFare))
				# print('Taxes: ' + str(self.taxes))
				# print('Departure date: ' + str(self.depDate))
				# print('Current date: ' + str(self.now))
				#print('Charge for Reissue: ' + )

				before = self.__set_values()

				summ = self.totalFare - before
				#return summ
				self.sum_fare = self.baseFare - before
				self.total = self.totalFare - before - self.non_refundable_taxes

				output = {}
				output['non_refundable taxes'] = self.non_refundable_taxes
				output['penalty'] = before
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

	def __set_values(self):
		words = self.rules.split('\n')
		
		cancellation = []

		#print(words)
		ch = 0
		for rule in words:
			#print(rule)
			if "CHANGES" in rule:
			 	ch = 1
			elif "CANCELLATIONS" in rule:
			 	ch = 2

			if ch == 2:
				cancellation.append(rule)
		
		ch = 0
		for rule in cancellation:
			#print(rule)
			
			if "BEFORE DEPARTURE" in rule:
				ch = 1
			elif "AFTER DEPARTURE" in rule:
				ch = 2

			if "CHARGE KZT" in rule and ch == 1:
			
				bef = rule.split()[2]
				bef = int(bef.split('.')[0])
				#print(bef)

				break

		return bef

			# if 'CHANGES' in rule:
			# 	self.check = 1
			# 	self.before = int(rule[5])
			# 	print(rule)
			# elif 'CANCELLATIONS' in rule:
			# 	self.check = 2
				
			#break