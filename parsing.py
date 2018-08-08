import datetime
import json

class Parser:

	def __init__(self, booking, fare_rules):
		self.booking = booking
		self.fare_rule = fare_rules

		self.company_codes = self.__get_codes()
		self.total_fares = self.__get_total_fares()
		self.taxes = self.__get_taxes()
		self.base_fares = self.__get_base_fares()
		self.currencies = self.__get_currencies()
		self.dates = self.__get_dates()
		self.full_names = self.__get_full_names()

		self.rules = self.__get_rules()

		self.data = self.__get_data()

		self.cities = self.__get_cities()

	def __get_cities(self):
		cities = []

		try:
			fares = json.loads(self.fare_rule['tarif_xml'])['fares']

			for fare in fares:
				pair = {}

				pair['city_depart'] = fare['city_depart']
				pair['city_arrive'] = fare['city_arrive']

				cities.append(pair)

			# print(cities)

			return cities

		except:
			return [['Error', 'Error']]

	def __get_data(self):			# group all data by each person in one array
		if self.__check_pair():
			data = []

			for i in range(len(self.company_codes)):
				
				# print(self.total_fares[i])
				# print(self.base_fares[i])
				# print(self.taxes[i])
				# print(self.dates[i])
				# print(self.company_codes[i])
				# print(self.currencies[i])

				dt = {}

				try:
					dt['totalFare'] = self.total_fares[i]
				except:
					dt['totalFare'] = 'NA'

				try:
					dt['baseFare'] = self.base_fares[i]
				except:
					dt['baseFare'] = 'NA'

				try:
					dt['taxes'] = self.taxes[i]
				except:
					dt['taxes'] = ['NA']

				try:
					dt['dates'] = self.dates[i]
				except:
					dt['dates'] = 'NA'

				try:
					dt['company_codes'] = self.company_codes[i]
				except:
					dt['company_codes'] = 'NA'

				try:
					dt['currencies'] = self.currencies[i]
				except:
					dt['currencies'] = 'NA'

				try:
					dt['rules'] = self.rules
				except:
					dt['rules'] = 'NA'

				# print(str(dt))

				data.append(dt)
				
			# print(data)

			return data

		else:
			return {'Error': 'Pairs match'}	# exception in checking pair

	def __check_pair(self):		# check for valid pair of booking and fare_rule
		return self.booking['cid'] == self.fare_rule['combination_id']

	def __get_codes(self):			# get codes of airline companies in array
		codes = []

		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

			for booking in bookings:
				try:
					code = booking['Routes'][0]['OperatingAirlineCode']

					# print(code)

					codes.append(code)

				except:
					codes.append('Error')	# exception in getting single airline code

			# print(codes)

			return codes

		except:
			return ['Error']			# exception in getting passes from booking

	def __get_total_fares(self):		# get total fares of bookings in array
		total_fares = []

		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

			for booking in bookings:
				try:
					total_fare = int(booking['TotalFare'])

					# print(total_fare)

					total_fares.append(total_fare)

				except:
					total_fares.append(-1)	# exception in getting single total fare

			# print(total_fares)

			return total_fares

		except:
			return [-1]				# exception in getting passes from booking

	def __get_taxes(self):			# get taxes grouped by each person in array as arrays of arrays of its type and amount
		values = []
		
		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

			for booking in bookings:
				value = []

				try:

					taxes = booking['Taxes']

					for tax in taxes:
						data = {}

						try:
							data['Type'] = tax['CountryCode']
							data['Amount'] = int(tax['Amount'])

							value.append(data)

						except:
							value.append(['Error', -1])	# exception in getting single tax from taxes

					values.append(value)

				except:
					values.append([['Error', -1]])		# exception in getting single taxes from booking
		
			# print(valuess)

			return values

		except:
			return [[['Error', -1]]]		# exception in getting passes from booking

	def __get_base_fares(self):		# calculating base fares arelying to total fares and taxes
		base_fares = []

		for i in range(len(self.total_fares)):
			try:

				if self.total_fares[i] != -1 and self.taxes[i] != [['Error', -1]]:
					base_fare = self.total_fares[i]

					for taxes in self.taxes[i]:
						# print(taxes)

						try:
							base_fare -= int(taxes['Amount'])

						except:
							base_fare = base_fare		# exception in getting single tax value
							

					# print(base_fare)

					base_fares.append(base_fare)

				else:
					base_fares.append(-1)		# # exception in checking total fare and taxes

			except:
				base_fares.append(-1)		# exception in getting i-th element

		return base_fares

	def __get_currencies(self):
		currencies = []

		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

			for booking in bookings:
				try:
					currency = booking['TotalFareCurrency']

					# print(currency)

					currencies.append(currency)

				except:
					currencies.append('Error')		# exception in getting single currency

			return currencies

		except:
			return ['Error']	# exception in getting passes from booking

	def __get_rules(self):			# get text of rules for penalties
		try:
			ruless = json.loads(self.fare_rule['tarif_xml'])['rules']
			texts = []

			for rules in ruless:
				try:
					text = ''

					for rule in rules:
						if rule['rule_title'] == 'PENALTIES':
							text += rule['rule_text']

					text = text.replace('        ', '').replace('       ', '').replace('      ', '')
					text = text.replace('     ', '').replace('    ', '').replace('   ', '')
					text = text.replace('  ', '').replace(' <br>', '')

					texts.append(text)

				except:
					pass

			return texts

		except:
			return 'Error'			# exception in getting tarif_xml from fare_rules

	def __get_dates(self):			# get current and departure date
		dates = []

		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

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
					dates.append(['Error', 'Error'])	# exception in getting single date pair

			return dates

		except:
			return [['Error', 'Error in booking passes']]	# exception in getting passes from booking

	def __cast_date(self, date):	# auxillary function for dates
		cast_date = date[0].split("-", 2)

		time = date[1].split(":", 2)

		cast_date = datetime.datetime(int(cast_date[0]), int(cast_date[1]), int(cast_date[2]), 
			int(time[0]), int(time[1]), int(time[2]))

		return cast_date

	def __get_full_names(self):
		full_names = []

		try:
			bookings = json.loads(self.booking['js_ticket'])['passes']

			for booking in bookings:
				try:
					given_name = booking['GivenName']

				except:
					given_name = ''		# exception in getting single given name

				try:
					sur_name = booking['Surname']

				except:
					sur_name = ''		# exception in getting single  surname

				if sur_name != '' and given_name != '':
					full_name = given_name + ' ' + sur_name

				elif sur_name != '':
					full_name = sur_name

				elif given_name != '':
					full_name = given_name

				else:
					full_name = ''

				full_names.append(full_name)

			return full_names

		except:
			return ['Error']	# exception in getting passes from booking

	def calculate_all(self):
		# print(self.data)

		result = []

		for i in range(len(self.data)):
			# print(self.data[i])

			if self.data[i] == {'Error': 'Pairs match'}:
				continue

			dts = []

			for text in self.data[i]['rules']:
				dt = self.data[i]

				dt['rules'] = text

				# print(dt)

				dts.append(dt)

			ress = []

			for dt in dts:
				res = self.__calculate(dt)

				ress.append(res['refunded_total'])

				print(res['refunded_total'])

			# print(ress.index(max(ress)))

			dt = self.__calculate(dts[ress.index(max(ress))])

			# print(dt)

			data = {}

			try:
				data['full_name'] = self.full_names[i]

			except:
				data['full_name'] = 'NA'			# exception in getting single full name

			try:
				data['departure_date'] = str(self.dates[i][1])

			except:
				data['departure_date'] = 'NA'

			try:
				data['cities'] = self.cities

			except:
				data['cities'] = 'NA'

			inner_data = {}

			try:
				inner_data['total_fare'] = self.total_fares[i]
			except:
				inner_data['total_fare'] = 'NA'	# exception in getting single total fare

			try:
				inner_data['base_fare'] = self.base_fares[i]
			except:
				inner_data['base_fare'] = 'NA'	# exception in getting single base fare

			try:
				inner_data['total_taxes'] = self.total_fares[i] - self.base_fares[i]
			except:
				inner_data['total_taxes'] = 'NA'	# exception in getting single total taxes

			try:
				inner_data['taxes'] = self.taxes[i]
			except:
				inner_data['taxes'] = 'NA'		# exception in getting single taxes

			try:
				inner_data['non_refundable taxes'] = dt['non_refundable taxes']
			except:
				inner_data['non_refundable taxes'] = 'NA'		# exception in getting single nonrefundable taxes

			try:
				inner_data['penalty'] = dt['penalty']
			except:
				inner_data['penalty'] = 'NA'	# exception in getting single penalty
				
			try:		
				inner_data['refunded_fare'] = dt['refunded_fare']
			except:
				inner_data['refunded_fare'] = 'NA'	# exception in getting single refunded fare

			try:
				inner_data['refunded_taxes'] = dt['refunded_taxes']
			except:
				inner_data['refunded_taxes'] = 'NA'	# exception in getting single refunded taxes

			try:
				inner_data['refunded_total'] = dt['refunded_total']
			except:
				inner_data['refunded_total'] = 'NA'	# exception in getting single total refund

			try:
				inner_data['operating_company'] = dt['name']
			except:
				inner_data['operating_company'] = 'NA'	# exception in getting single operating company

			try:
				inner_data['currency'] = self.currencies[i]
			except:
				inner_data['currency'] = 'NA'		# exception in getting single currency

			data['data'] = inner_data

			result.append(data)

		return result

	def __calculate(self, data):		# main function of this class, parses code of company and calculates charge
		# print(data['totalFare'])
		# print(data['baseFare'])
		# print(data['rules'])
		# print(data['taxes'])
		# print(data['company_codes'])
		# print(data['currencies'])
		# print(data['dates'])

		if data['totalFare'] != -1 and data['baseFare'] != -1 and data['rules'] != '' and data['taxes'] != [['Error']] and data['company_codes'] != 'Error' and data['currencies'] != 'Error' and data['dates'] != ['Error', 'Error']:

			comp =	 None

			if data['company_codes'] == 'DV':	# Scat`s code
				from scat import Scat
				comp = Scat(data)

			elif data['company_codes'] == 'Z9':	# BekAir`s code
				from bekair import BekAir
				comp = BekAir(data)

			elif data['company_codes'] == 'SU':	# Aeroflot`s code
				from aeroflot import Aeroflot
				comp = Aeroflot(data)

			elif data['company_codes'] == 'HY':	# Uzbekistan`s code
				from uzbekistan import Uzbekistan
				comp = Uzbekistan(data)
			
			elif data['company_codes'] == 'TK':	# Turkish`s code
				from turkish import Turkish
				comp = Turkish(data)

			try:
				return comp.calculate()

			except:
				return {'Error': 'Error in class calculation'}	# exception in class calculate
		else:
			return {'Error': 'Error in value check'}	# exception in value check