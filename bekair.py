import xml.dom.minidom

class BekAir():
 
	def __init__(self, data):
		self.totalFare = int(data['totalFare'])		
		self.baseFare = int(data['baseFare'])
		self.rules = data['rules']					
		self.taxes = data['taxes']					
		self.now = data['dates'][0]					
		self.depDate = data['dates'][1]	

		self.mode = ' '
		self.check = 0  
		#self.arr_rules = []
		self.before = 0

	def calculate(self):

		if self.before == 0:

			if self.__get_status():

				print('Total fare: ' + str(self.totalFare))
				print('Base fare: ' + str(self.baseFare))
				print('Taxes: ' + str(self.taxes))
				print('Departure date: ' + str(self.depDate))
				print('Current date: ' + str(self.now))
				#print('Charge for Reissue: ' + )

				before = self.__set_values()

				summ = self.totalFare - before
				return summ
			return 'Error'
		return 'Error'	

	def __get_status(self):
		return self.now < self.depDate 

	def __set_values(self):
		words = self.rules.split('\n')
		#print(words)
		ch = 0
		for rule in words:
			 if "CHANGES" in rule:
			 	ch = 1
			 elif "CANCELLATIONS" in rule:
			 	ch = 2
			 elif "BEFORE DEPARTURE" in rule:
			 		ch = 3
			 if "CHARGE KZT" in rule and ch == 3:
			 		#print(rule.split()[2])
			 		bef = rule.split()[2]
			 		bef = int(bef.split('.')[0])
			 		print(bef)
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

	
				