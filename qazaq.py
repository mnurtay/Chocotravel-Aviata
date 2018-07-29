import datetime

class Qazaq:

	def __init__(self, data):
		self.totalFare = int(data['totalFare'])		# total fare ok booking
		self.baseFare = int(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date

		self.coef = -1						# double between 0-1 or -1

		self.__set_coef()					# setting coef

		self.non_ref = ['YR', 'YQ']			# array of nonrefundable taxes` types

	def calculate(self):
		if self.coef != -1 and self.coef != 1:					# check for errors and nonrefundable tarifs

			if self.__check_status():							# check status
				non_ref = self.__calc_taxes()

				print(non_ref)

				summ = self.totalFare - self.baseFare * self.coef - non_ref

				return summ

			return 'Error'				# return error

		return 'Error'					# return error

	def __calc_taxes(self):				# get nonrefundable taxes
		non_ref = 0

		for tax in self.taxes:
			if tax[0] in self.non_ref:
				non_ref += int(tax[1])

		return non_ref

	def __check_status(self):			# check status of flight
		return self.now < self.depDate

	def __set_coef(self):				# set coef of charge
		lines = self.rules.split('\n')

		for line in lines:
			words = line.split(' ')
			if 'Возврат' in words[0]:
				if 'не' in words:
					self.coef = 1

				else:
					num = int(words[4].replace('%', ''))
					self.coef = num / 100

				break
