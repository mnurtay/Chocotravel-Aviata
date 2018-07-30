import datetime
import json

class Parser:

	def __init__(self, booking, fare_rules):
		self.booking = json.loads(booking)
		self.fare_rule = json.loads(fare_rules)

		self.company_codes = self.__get_codes()
		self.total_fares = self.__get_total_fares()
		self.taxes = self.__get_taxes()
		self.base_fares, self.total_taxes = self.__get_base_fares_total_taxes()
		self.currencies = self.__get_currencies()
		self.dates = self.__get_dates()
		self.full_names = self.__get_full_names()

		self.rules = self.__get_rules()

		self.data = self.__get_data()

	def __get_data(self):
		if self.__check_pair():
			data = []

			for i in range(len(company_codes)):
				try:
					dt = {
						'totalFare': self.total_fares[i],
						'baseFare': self.base_fares[i],
						'taxes': self.taxes[i]
						'dates': self.dates[i]
						'company_codes': self.company_codes[i]
						'rules': self.rules
					}

					data.append(dt)

				except:
					data.append('Error')

			return data

		else:
			return ['Error']

	def __check_pair(self):
		return self.booking['cid'] == self.fare_rule['combination_id']

	def __get_codes(self):			# get code of airline company
		codes = []

		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				try:
					code = booking['Routes'][0]['OperatingAirlineCode']

					# print(code)

					codes.append(code)

				except:
					codes.append('Error')

			# print(codes)

			return codes

		except:
			return ['Error']			# return exception as string 'Error'

	def __get_total_fares(self):		# get total fare of booking
		total_fares = []

		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				try:
					total_fare = int(booking['TotalFare'])

					# print(total_fare)

					total_fares.append(total_fare)

				except:
					total_fares.append(-1)

			print(total_fares)

			return total_fares

		except:
			return [-1]				# return exception as -1

	def __get_taxes(self):			# get taxes as array of arrays of its type and amount
		valuess = []
		
		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				values = []

				try;

					taxes = booking['Taxes']

					for tax in taxes:
						value = []

						try:

							value.append(tax['CountryCode'])
							value.append(tax['Amount'])

							values.append(value)

						except:
							values.append(['Error', -1])

					valuess.append(values)

				except:
					valuess.append([['Error', -1]])
		
			# print(valuess)

			return valuess

		except:
			return [[['Error', -1]]]		# return exception as [[['Error']]]

	def __get_base_fares_total_taxes(self):		# calculating base fare according to total fare and taxes
		base_fares = []
		total_taxes = []

		for i in range(len(self.total_fares)):
			try:

				if self.total_fares[i] != -1 and self.taxes[i] != [['Error', -1]]:
					base_fare = self.total_fares[i]
					total_tax = 0

					for taxes in self.taxes[i]:
						for tax in taxes:
							try:
								base_fare -= int(tax[1])
								total_tax += int(tax[1])

							except:
								base_fare = base_fare
								total_tax = total_taxes

					# print(base_fare)
					# print(total_tax)

					base_fares.append(base_fare)
					total_taxes.append(total_tax)

				else:
					base_fares.append(-1)
					total_taxes.append(-1)

			except:
				base_fares.append(-1)
				total_taxes.append(-1)

		return base_fares, total_taxes

	def __get_currencies(self):
		currencies = []

		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				try:
					currency = booking['TotalFareCurrency']

					# print(currency)

					currencies.append(currency)

				except:
					currencies.append('Error')

			return currencies

		except:
			return ['Error']

	def __get_rules(self):			# get text of rules for penalties
		try:
			rules = self.fare_rule['tarif_xml']['rules'][0]
			text = ''

			for rule in rules:
				if rule['rule_title'] == 'PENALTIES':
					text += rule['rule_text']

			text = text.replace('        ', '').replace('       ', '').replace('      ', '')
			text = text.replace('     ', '').replace('    ', '').replace('   ', '')
			text = text.replace('  ', '').replace(' <br>', '')

			# print(text)

			return text

		except:
			return 'Error'			# return exception as string 'Error'

	def __get_dates(self):			# get current and departure date
		dates = []

		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				try:

					departureDate = booking['Routes'][0]['DepartureDate']
					currentDate = datetime.datetime.now().isoformat()

					# split string
					departureDate = departureDate.split("T", 1)
					currentDate = currentDate.split("T", 1)
					currentDate[1] = currentDate[1].split(".", 1)[0]

					# castDate
					departureDate = self.__cast_date(departureDate)
					currentDate = self.__cast_date(currentDate)

					dates.append([currentDate, departureDate])

				except:
					dates.append(['Error', 'Error'])

			return dates

		except:
			return [['Error', 'Error']]

	def __cast_date(self, date):	# auxillary function for dates
		cast_date = date[0].split("-", 2)

		time = date[1].split(":", 2)

		cast_date = datetime.datetime(int(cast_date[0]), int(cast_date[1]), int(cast_date[2]), 
			int(time[0]), int(time[1]), int(time[2]))

		return cast_date

	def __get_full_names(self):
		full_names = []

		try:
			bookings = self.booking['js_ticket']['passes']

			for booking in bookings:
				try:
					given_name = booking['GivenName']

				except:
					given_name = ''

				try:
					sur_name = booking['Surname']

				except:
					sur_name = ''

				if sur_name == '' and given_name == '':
					full_name = ''

				elif sur_name == '':
					full_name = given_name

				elif given_name == '':
					full_name = sur_name

				else:
					full_name = given_name + ' ' + sur_name

				full_names.append(full_name)

		except:
			return ['Error']

	def calculate_all(self):
		result = []

		for i in range(len(self.data)):
			try:
				dt = self.__calculate(self.data[i])

				data = {}

				try:
					data['full_name'] = self.full_names[i]

				except:
					data['full_name'] = ''

				inner_data = {}

				try:
					inner_data['total_fare'] = self.total_fares[i]
					inner_data['base_fare'] = self.base_fares[i]
					inner_data['total_taxes'] = self.total_taxes[i]
					inner_data['taxes'] = self.taxes[i]
					inner_data['non_refundable taxes'] = dt['non_refundable taxes']
					inner_data['penalty'] = dt['penalty']
					inner_data['refunded_fare'] = dt['refunded_fare']
					inner_data['refunded_taxes'] = dt['refunded_taxes']
					inner_data['refunded_total'] = dt['refunded_total']
					inner_data['operating_company'] = dt['name']
					inner_data['currency'] = self.currencies[i]

				except:
					inner_data = {'Error': 'Error'}

				data['data'] = inner_data

				result.append(dt)

			except:
				result.append('Error': 'Error')

		return result

	def __calculate(self, data):		# main function of this class, parses code of company and calculates charge
		if data['totalFare'] != -1 and data['baseFare'] != -1 and data['rules'] != 'Error' and data['taxes'] != [['Error']] and data['company_codes'] != 'Error':

			comp = None

			if self.companyCode == 'DV':	# Scat`s code
				from scat import Scat
				
				comp = Scat(data)

			elif self.companyCode == 'Z9':	# BekAir`s code
				from bekair import BekAir

				comp = BekAir(data)

			elif self.companyCode == 'SU':	# Aeroflot`s code
				from aeroflot import Aeroflot

				comp = Aeroflot(data)

			elif self.companyCode == 'SU':	# Uzbekistan`s code
				from uzbekistan import Uzbekistan

				comp = Uzbekistan(data)

			try:
				return comp.calculate()

			except:
				return {'Error': 'Error'}
		else:
			return {'Error': 'Error'}