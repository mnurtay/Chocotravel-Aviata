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

		print('Total fare is ' + str(self.totalFare))
		print('Base fare is ' + str(self.baseFare))
		print('Taxes are ' + str(self.taxes))
		print('Departure date is ' + str(self.depDate))

		self.dom = True

		self.__set_values()

		# print('Fare rules is ' + str(self.rules))

		self.non_ref = ['YR']				# array of nonrefundable taxes` types

	def calculate(self):
		pass
		

	def __calc_coef(self):			# get coef of charge
		pass

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

	def __set_values(self):						# set values for calculating change
		ps = self.rules.split('\n\n')

		# print(ps)

		if 'BETWEEN' in ps[0]:
			self.dom = False

		for p in ps:
			qwe = self.__split_all(p)
		
			# print(qwe)

			if 'CANCELLATIONS' in qwe and 'REFUND' in qwe and 'AFTER' not in qwe:
				for qw in qwe:
					if self.__is_number(qw):
						self.charge = qw

					elif self.__is_currency(qw):
						self.charge_cur = qw

		print(self.charge)
		print(self.charge_cur)
		# print(ps)

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

	def __is_number(self, text):
		try:
			a = float(text)
			# print(a)
			return True

		except:
			return False

	def __is_currency(self, text):
		if text == 'EUR' or text == 'USD' or text == 'KZT' or text == 'UZS':
			return True

		return False