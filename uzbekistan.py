import datetime

class Uzbekistan:

	def __init__(self, data):
		self.totalFare = int(data['totalFare'])		# total fare ok booking
		self.baseFare = int(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date

		print('Total fare is ' + str(self.totalFare))
		print('Base fare is ' + str(self.baseFare))
		print('Taxes are ' + str(self.taxes))
		print('Departure date is ' + str(self.depDate))

		self.__set_values()

		print(self.rules)

		
	def calculate(self):
		return 'Error'

	def __set_values(self):
		lines = self.rules.split('\n')

		# print(lines)