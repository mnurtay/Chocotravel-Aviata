import datetime

class Qazaq:

	def __init__(self, totalFare, baseFare, rules, taxes, dates):
		self.totalFare = int(totalFare)		# total fare ok booking
		self.baseFare = int(baseFare)		# base fare of booking
		self.rules = rules					# text of fare rules
		self.taxes = taxes					# array of pairs type of taxe and its amount
		self.now = dates[0]					# current date
		self.depDate = dates[1]				# departure date

		self.tarif = 'Error'

		self.__set_tarif()					# setting tarif

		self.non_ref = ['YR', 'YQ']			# array of nonrefundable taxes` types

	def calculate(self):
		if self.tarif != 'Error' and self.tarif != 'B':			# check for errors and nonrefundable tarifs
			if self.__check_status():							# check status
				print(self.tarif)

				coef = self.__calc_coef()

				print(coef)

				non_ref = self.__calc_taxes()

				print(non_ref)

				summ = self.totalFare - self.baseFare * coef - non_ref

				return summ

			self.tarif = 'Error'	
			return self.tarif			# return error

		self.tarif = 'Error'
		return self.tarif				# return error

	def __calc_coef(self):				# get coef for charge
		coef = 0

		if self.tarif == 'S':
			coef = 0.3

		return coef

	def __calc_taxes(self):				# get nonrefundable taxes
		non_ref = 0

		for tax in self.taxes:
			if tax[0] in self.non_ref:
				non_ref += int(tax[1])

		return non_ref

	def __check_status(self):			# check status of flight
		return self.now < self.depDate

	def __set_tarif(self):				# set tarif of flight
		words = self.rules.split(' ')

		self.tarif = words[0]			# get the first letter of flight

