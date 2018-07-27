import datetime

class Scat:

	def __init__(self, totalFare, baseFare, rules, taxes, dates):
		self.totalFare = int(totalFare)		# total fare ok booking
		self.baseFare = int(baseFare)		# base fare of booking
		self.rules = rules					# text of fare rules
		self.taxes = taxes					# array of pairs type of taxe and its amount
		self.now = dates[0]					# current date
		self.depDate = dates[1]				# departure date

		self.minutes = -1					# time gap for rules
		self.first = -1						# first mode change
		self.second = -1					# second mode change

		self.__set_data()					# setting main values

		self.ref = ['XR']					# array of refundable taxes` types
		self.non_ref = ['YR']				# array of nonrefundable taxes` types
		self.mode = 'Error'					# mode ('before/before', 'before/after', 'Error')

	def calculate(self):
		if self.minutes != -1 and self.first != -1 and self.second != -1:
			if self.__check_status_Scat():
				# print(self.taxes)
				# print(self.mode)

				coef = self.__calc_coef()

				print(coef)

				non_ref = self.__calc_taxes()

				# print(coef * self.baseFare)
				# print(non_ref)

				summ = self.totalFare - coef * self.baseFare - non_ref

				return summ

			return self.mode

		return self.mode

	def __calc_coef(self):
		coef = 0

		if self.mode == 'before/before':
			return int(self.first) / 100

		elif self.mode == 'before/after':
			return int(self.second) / 100

	def __calc_taxes(self):
		non_ref = 0

		for tax in self.taxes:
			if tax[0] in self.non_ref:
				non_ref += int(tax[1])

		return non_ref

	def __check_status_Scat(self):
		timedelta = 0

		if self.minutes == 90:
			timedelta = datetime.timedelta(minutes=30, hours=1)

		elif self.minutes == 180:
			timedelta = datetime.timedelta(hours=3)

		# print(self.now)
		# print(timedelta)
		# print(self.depDate)

		if self.now + timedelta < self.depDate:
			self.mode = 'before/before'

		elif abs(self.now - self.depDate) < timedelta:
			self.mode = 'before/after'

		return self.now < self.depDate or (self.depDate + timedelta) > self.now

	def __set_data(self):						# get tarif`s name from fare_rule_text
		words = self.rules.split(' ')

		try:
			first_word = words[1].split('.')[2]			# get first_word of fare_rule_texxt
		except:
			first_word = ''

		if first_word == 'PERMITTED':					# 'Flexible' tarif`s text begins with 'PERMITTED'
			self.minutes = 0
			self.first = 0
			self.second = 0

		elif first_word == 'CHANGES':					# other tarif`s text begins with 'CHANGES'
			try:										# try to define minutes
				self.minutes = int(words[4])
			except:
				self.minutes = -1

			try:										# try to define first_charge
				self.first = int(words[11].split('\n')[0])
			except:
				self.first = -1

			try:										# try to define second_charge
				self.second = int(words[26])
			except:
				self.second = -1