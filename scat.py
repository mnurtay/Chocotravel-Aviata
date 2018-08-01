import datetime

class Scat:

	def __init__(self, data):
		self.name = 'SCAT Airlines'

		self.totalFare = int(data['totalFare'])		# total fare ok booking
		self.baseFare = int(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date
		self.currency = data['currencies']

		self.minutes = -1					# time gap for rules
		self.first = -1						# first mode change
		self.second = -1					# second mode change

		# print('Total fare is ' + str(self.totalFare))
		# print('Base fare is ' + str(self.baseFare))
		# print('Taxes are ' + str(self.taxes))
		# print('Departure date is ' + str(self.depDate))


		# print('Fare rules is ' + str(self.rules))
		
		self.__set_values()					# setting main values

		# print('Special values are ' + str(self.minutes) + ', ' + str(self.first) + ', ' + str(self.second))

		self.non_ref = ['YR']				# array of nonrefundable taxes` types
		self.mode = 'Error'					# mode ('before/before', 'before/after', 'Error')

	def calculate(self):
		# print(self.minutes)
		# print(self.first)
		# print(self.second)
		if self.minutes != -1 and self.first != -1 and self.second != -1:	# check for values
		
			if self.__check_status():										# check status

				# print('Total fare is ' + str(self.totalFare))
				# print('Base fare is ' + str(self.baseFare))
				# print('Taxes are ' + str(self.taxes))
				# print('Departure date is ' + str(self.depDate))

				coef = self.__calc_coef()

				self.penalty = coef * self.baseFare

				# print('Coeficient of charge is ' + str(coef))

				# print(self.__calc_taxes())

				self.non_ref, self.ref = self.__calc_taxes()

				# print('Non refundable taxes are ' + str(self.non_ref))
				# print('Non refundable part is ' + str(non_ref))

				self.total = self.totalFare - self.penalty - self.non_ref	# total returned sum

				data = {}
				data['non_refundable taxes'] = self.non_ref
				data['penalty'] = self.penalty

				data['refunded_fare'] = self.baseFare - self.penalty
				data['refunded_taxes'] = self.ref
				data['refunded_total'] = self.total
				data['name'] = self.name

				# print(data)

				return data

			return {'Error': 'Error'}		# return error

		return {'Error': 'Error'}			# return error

	def __calc_coef(self):			# get coef of charge
		coef = 0

		if self.mode == 'before/before':
			return int(self.first) / 100

		elif self.mode == 'before/after':
			return int(self.second) / 100

	def __calc_taxes(self):			# get nonrefundable taxes
		non_ref = 0
		ref = 0

		for tax in self.taxes:
			if tax['Type'] in self.non_ref:
				non_ref += int(tax['Amount'])

			else:
				ref += int(tax['Amount'])

		return non_ref, ref

	def __check_status(self):		# check status of flight
		timedelta = 0

		if self.minutes == 90:
			timedelta = datetime.timedelta(minutes=30, hours=1)

		elif self.minutes == 180:
			timedelta = datetime.timedelta(hours=3)

		# print('Today`s date is ' + str(self.now))
		# print('Timedelta is ' + str(timedelta))
		# print('Departure date is ' + str(self.depDate))

		if self.now + timedelta < self.depDate:
			self.mode = 'before/before'

		elif self.now + timedelta >= self.depDate:
			self.mode = 'before/after'

		# print(self.now < self.depDate)

		return self.now < self.depDate

	def __set_values(self):						# set values for calculating change
		lines = self.rules.split('\n')

		# print(lines)

		try:
			first_word = lines[2].split('.')[2].split(' ')[0]		# get first_word of fare_rule_text
		except:
			first_word = ''

		if first_word == 'PERMITTED':					# 'Flexible' tarif`s text begins with 'PERMITTED'
			self.minutes = 0
			self.first = 0
			self.second = 0

		elif first_word == 'CHANGES':					# other tarif`s text begins with 'CHANGES'
			try:										# try to define minutes
				self.minutes = int(lines[3].split(' ')[2])
			except:
				self.minutes = -1

			try:										# try to define first_charge
				self.first = int(lines[4].split(' ')[4])
			except:
				self.first = -1

			try:										# try to define second_charge
				self.second = int(lines[9].split(' ')[2])
			except:
				self.second = -1