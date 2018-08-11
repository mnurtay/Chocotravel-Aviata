from converter import Converter
from validator import Validator

class Uzbekistan:

	def __init__(self, data):
		self.name = 'Uzbekistan Airways'

		self.totalFare = int(data['totalFare'])		# total fare ok booking
		self.baseFare = int(data['baseFare'])		# base fare of booking
		self.rules = data['rules']					# text of fare rules
		self.taxes = data['taxes']					# array of pairs type of taxe and its amount
		self.now = data['dates'][0]					# current date
		self.depDate = data['dates'][1]				# departure date
		self.currency = data['currencies']

		self.charge = ''
		self.charge_cur = ''
		self.percent = False
		self.penalty = ''

		# print('Total fare is ' + str(self.totalFare))
		# print('Base fare is ' + str(self.baseFare))
		# print('Taxes are ' + str(self.taxes))
		# print('Departure date is ' + str(self.depDate))
		# print(self.currency)

		# print(self.rules)

		self.dom = True

		self.__set_values()

		# print('Fare rules is ' + str(self.rules))

		self.non_ref = []				# array of nonrefundable taxes` types

	def calculate(self):
		c = Converter()

		# print(c.currencies())

		if self.__check_status():

			if self.charge != '' and self.charge_cur != '':
				# print(self.charge_cur)
				# print(self.charge)
				# print(self.currency)

				self.penalty = c.calc(self.charge_cur, float(self.charge), self.currency)

				# print(self.penalty)
				
			elif self.charge != '' and self.percent:
				self.penalty = round(self.baseFare * self.percent / 100)

			# print(self.penalty)

			self.non_ref_tax, self.ref_tax = self.__calc_taxes()

			self.total = self.totalFare - self.penalty - self.non_ref_tax

			data = self.__get_data()

			return data

	def __get_data(self):
		data = {}

		data['non_refundable taxes'] = self.non_ref
		data['penalty'] = self.penalty

		data['refunded_fare'] = self.baseFare - self.penalty
		data['refunded_taxes'] = self.ref_tax
		data['refunded_total'] = self.total
		data['name'] = self.name

		return data

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
		return self.now < self.depDate

	def __set_values(self):
		v = Validator()

		ps = self.rules.split('\n\n')

		# print(ps)

		if 'BETWEEN' in ps[0] and 'UZBEKISTAN' in ps[0]:
			self.dom = False
	
		for p in ps:
			
			p = p.replace('\n', ' ').replace('  ', ' ')
			# print(p)
			# print()
			if self.dom:
				if 'REFUND' in p and 'CANCELLATION' in p and 'CHANGES' not in p:
					qwe = p.split('.')

					for qw in qwe:
						if 'REFUND' in qw and 'CHARGE' in qw:
							for i in range(len(qw)):
								if v.is_number(qw[i]):
									self.charge = qw[i]

									if v.is_percent(qw[i+1]):
										self.percent = True

										break

								if v.is_percent(qw[i]):
									self.percent = True
							break

					# print(self.charge, '%')

					break


			else:
				if 'CANCELLATIONS PERMITTED' in p and 'BEFORE DEPARTURE' in p and 'REFUND' in p:
					# print(p)
					# print(len(p))
					
					s = list(p)

					for i in range(1, len(s) - 1):
						if s[i] == '.' and not v.is_number(s[i-1]) and not v.is_number(s[i+1]):
							s[i] = ''

					p = ''.join(s)

					qwe = p.split(' ')

					i = qwe.index('CHARGE')

					if v.is_currency(qwe[i+1]):
						self.charge_cur = qwe[i+1]

						if v.is_number(qwe[i+2]):
							self.charge = qwe[i+2]

						else:
							for qw in qwe:
								if v.is_number(qw):
									self.charge = qwe[i+1]
									break

					#print(self.charge, self.charge_cur)

					break

	def __split_all(self, p):
		qwe = []

		wordsss = p.split('\n')

		for wordss in wordsss:

			words = wordss.split(' ')

			for word in words:
				if not self.__is_number(word):
					word = word.replace('.', '')
				qwe.append(word)

		return qwe