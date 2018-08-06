import requests
import bs4

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

		print('Total fare is ' + str(self.totalFare))
		print('Base fare is ' + str(self.baseFare))
		print('Taxes are ' + str(self.taxes))
		print('Departure date is ' + str(self.depDate))
		print(self.currency)

		self.dom = True

		# self.__set_values()
		self.__set_values1()

		# print('Fare rules is ' + str(self.rules))

		self.non_ref = []				# array of nonrefundable taxes` types

	def calculate(self):
		if self.__check_status():
			
			if self.charge != '' and self.charge_cur != '':
				self.penalty = round(self.__get_Exchange_Rates(self.charge_cur, self.charge))

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

	def __get_Exchange_Rates(self, course, amount):
		site = requests.get('https://prodengi.kz/currency/')
		html = bs4.BeautifulSoup(site.text, "html.parser")
		price = None
		if course=="EUR" or course=="RUB" or course=="USD":
			tenge = html.select('.content_list .'+course+' .price_buy')
			# print(tenge)
			price = tenge[0].getText()
			price = float(price) * float(amount)
		return price
	
	def __set_values1(self):
		ps = self.rules.split('\n\n')

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
								if self.__is_number(qw[i]):
									self.charge = qw[i]

									if self.__is_percent(qw[i+1]):
										self.percent = True

										break

								if self.__is_percent(qw[i]):
									self.percent = True
							break

					print(self.charge, '%')

					break


			else:
				if 'CANCELLATIONS PERMITTED' in p and 'BEFORE DEPARTURE' in p and 'REFUND' in p:
					# print(p)
					# print(len(p))
					
					s = list(p)

					for i in range(1, len(s) - 1):
						if s[i] == '.' and not self.__is_number(s[i-1]) and not self.__is_number(s[i+1]):
							s[i] = ''

					p = ''.join(s)

					qwe = p.split(' ')

					i = qwe.index('CHARGE')

					if self.__is_currency(qwe[i+1]):
						self.charge_cur = qwe[i+1]

						if self.__is_number(qwe[i+2]):
							self.charge = qwe[i+2]

						else:
							for qw in qwe:
								if self.__is_number(qw):
									self.charge = qwe[i+1]
									break

					print(self.charge, self.charge_cur)

					break

	def __set_values(self):						# set values for calculating change
		ps = self.rules.split('\n\n')

		# print(ps)

		if 'BETWEEN' in ps[0]:
			self.dom = False

		for p in ps:
			qwe = self.__split_all(p)

			if self.dom:
				if 'CANCELLATION' in qwe and 'REFUND' in qwe:
					for qw in qwe:
						if self.__is_number(qw):
							self.charge = qw

						elif self.__is_percent(qw):
							self.percent = True

			else:
				if 'CANCELLATIONS' in qwe and 'REFUND' in qwe and 'AFTER' not in qwe:
					for qw in qwe:
						if self.__is_number(qw):
							self.charge = qw

						elif self.__is_currency(qw):
							self.charge_cur = qw

		# if self.dom:
		# 	if self.percent:
		# 		print(self.charge + '%')

		# else:
		# 	print(self.charge + ' ' + self.charge_cur)

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

	def __is_percent(self, text):
		if text == 'PERCENT' or text == 'PCT':
			return True

		return False

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