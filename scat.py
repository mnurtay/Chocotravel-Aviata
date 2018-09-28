import datetime

from validator import Validator

class Scat:

	def __init__(self, data):
		self.name = 'SCAT Airlines'

		self.totalFare = float(data['totalFare'])	# total fare ok booking
		self.baseFare = float(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date
		self.currency = data['currencies']

		self.minutes = -1					# time gap for rules
		self.first = -1						# first mode change
		self.second = -1					# second mode change

		self.__parse_data()					# parsing rules for data

		self.non_ref = ['YR']				# array of nonrefundable taxes` types
		self.mode = 'Error'					# mode ('before/before', 'before/after', 'Error')

		# print(self.rules)

	def calculate(self):
		# print(self.minutes)
		# print(self.first)
		# print(self.second)

		if self.__check_status():						# check status
		
			if self.minutes != -1 and self.first != -1 and self.second != -1:	# check for values

				coef = self.__calc_coef()

				self.penalty = coef * self.baseFare

				# print('Coeficient of charge is ' + str(coef))

				self.non_ref, self.ref = self.__calc_taxes()

				# print('Non refundable taxes are ' + str(self.non_ref))
				# print('Non refundable part is ' + str(non_ref))

				self.total = self.totalFare - self.penalty - self.non_ref	# total returned sum

				data = self.__get_data()

				# print(data)

				return data

			return {'Error': 'Fare rules'}		# return error

		return {'Error': 'Date'}			# return error
	
	def __get_data(self):
		data = {}

		data['non_refundable taxes'] = self.non_ref
		data['penalty'] = self.penalty

		data['refunded_fare'] = self.baseFare - self.penalty
		data['refunded_taxes'] = self.ref
		data['refunded_total'] = self.total
		data['name'] = self.name

		return data

	def __calc_coef(self):			# get coef of charge
		coef = 0

		if self.mode == 'before/before':
			coef = float(self.first) / 100

		elif self.mode == 'before/after':
			coef = float(self.second) / 100

		return coef

	def __calc_taxes(self):			# get nonrefundable and refundable taxes` sum
		non_ref = 0
		ref = 0

		for tax in self.taxes:
			if tax['Type'] in self.non_ref:
				non_ref += float(tax['Amount'])

			else:
				ref += float(tax['Amount'])

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

	def __parse_data(self):
		v = Validator()

		paragraphs = self.rules.split('\n\n')

		for paragraph in paragraphs:
			paragraph = paragraph.replace('\n', ' ').replace('  ', ' ')

			# print(paragraph)
			# print()

			if 'CANCELLATION' in paragraph and 'PERMITTED' in paragraph and 'BEFORE DEPARTURE NOTE' in paragraph:
				sentences = paragraph.split('.')

				for sentence in sentences:
					if 'MORE THAN' in sentence and 'BEFORE' in sentence and 'CHARGE' in sentence:
						# print(sentence)

						words = sentence.split(' ')

						i = words.index('THAN')

						# print(words[i+1])

						if not v.is_number(words[i+1]) and 'MINUTES' in words[i+1]:
							words[i+1] = words[i+1].replace('MINUTES', '')

						self.minutes = int(words[i+1])

						i = words.index('CHARGE')

						# print(words[i+1])

						if not v.is_number(words[i+1]) and 'PERCENT' in words[i+1]:
							words[i+1] = words[i+1].replace('PERCENT', '')

						self.first = float(words[i+1])

						# print(self.minutes, self.first)

					elif 'LESS THAN' in sentence and 'BEFORE' in sentence and 'CHARGE' in sentence:
						# print(sentence)

						words = sentence.split(' ')

						i = words.index('THAN')

						# print(words[i+1])

						if not v.is_number(words[i+1]) and 'MINUTES' in words[i+1]:
							words[i+1] = words[i+1].replace('MINUTES', '')

						self.minutes = int(words[i+1])

						i = words.index('CHARGE')

						# print(words[i+1])

						if not v.is_number(words[i+1]) and 'PERCENT' in words[i+1]:
							words[i+1] = words[i+1].replace('PERCENT', '')

						self.second = float(words[i+1])

						# print(self.minutes, self.second)