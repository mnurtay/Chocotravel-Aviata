import datetime

class Scat:

	def __init__(self, data):
		self.totalFare = int(data['totalFare'])		# total fare ok booking
		self.baseFare = int(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date

		self.minutes = -1					# time gap for rules
		self.first = -1						# first mode change
		self.second = -1					# second mode change

		# print(self.totalFare)
		# print(self.taxes)
		# print(self.depDate)
		# print(self.rules)
		
		self.__set_values()					# setting main values

		print(self.minutes, self.first, self.second)

		self.non_ref = ['YR']				# array of nonrefundable taxes` types
		self.mode = 'Error'					# mode ('before/before', 'before/after', 'Error')

	def calculate(self):
		if self.minutes != -1 and self.first != -1 and self.second != -1:	# check for values
		
			if self.__check_status():										# check status
				# print(self.taxes)
				# print(self.mode)

				coef = self.__calc_coef()

				print(coef)

				non_ref = self.__calc_taxes()

				print(non_ref)

				# print(coef * self.baseFare)
				# print(non_ref)

				summ = self.totalFare - coef * self.baseFare - non_ref	# total returned sum

				return summ

			return self.mode		# return error

		return self.mode			# return error

	def __calc_coef(self):			# get coef for charge
		coef = 0

		if self.mode == 'before/before':
			return int(self.first) / 100

		elif self.mode == 'before/after':
			return int(self.second) / 100

	def __calc_taxes(self):			# get nonrefundable taxes
		non_ref = 0

		for tax in self.taxes:
			if tax[0] in self.non_ref:
				non_ref += int(tax[1])

		return non_ref

	def __check_status(self):		# check status of flight
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

	def __set_values(self):						# set values for calculating change
		words = self.rules.split(' ')

		print(words)

		try:
			first_word = words[1].split('.')[2]			# get first_word of fare_rule_text
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
				self.first = int(words[12].split('\n')[0])
			except:
				self.first = -1

			try:										# try to define second_charge
				self.second = int(words[28])
			except:
				self.second = -1