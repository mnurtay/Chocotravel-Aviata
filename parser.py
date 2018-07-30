import datetime
import json

class Parser:

	def __init__(self, booking, fare_rules):
		self.booking = json.loads(booking)
		self.fareRule = json.loads(fare_rules)

		self.companyCode = self.__get_code()
		self.totalFare = self.__get_total_fare()
		self.taxes = self.__get_taxes()
		self.baseFare = self.__get_base_fare()
		self.currency = self.__get_currency()

		self.rules = self.__get_rules()

	def __get_data(self):
		if self.__check_pair():
			self.booking = self.booking['js_ticket']
			self.fareRule = self.fareRule['tarif_xml']

			data = []

			for booking in self.booking['passes']:



		else:
			return 'Not valid pair!'

	def __check_pair(self):
		return self.booking['cid'] == self.fareRule['combination_id']

	def __get_codes(self):			# get code of airline company
		codes = []

		try:
			bookings = self.booking['passes']

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
			bookings = self.booking['passes']

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
			bookings = self.booking['passes']

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

	def __get_base_fares(self):		# calculating base fare according to total fare and taxes
		base_fares = []

		for i in range(len(self.total_fares)):
			try:

				if self.total_fares[i] != -1 and self.taxes[i] != [['Error', -1]]:
					base_fare = self.total_fares[i]

					for taxes in self.taxes[i]:
						for tax in taxes:
							try:
								base_fare -= int(tax[1])

							except:
								base_fare = base_fare

					# print(base_fare)

					base_fares.append(base_fare)

				else:
					base_fares.append(-1)

			except:
				base_fares.append(-1)

		return base_fares

	def __get_currencies(self):
		currencies = []

		try:
			bookings = self.booking['passes']

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
			rules = self.fareRule['rules'][0]
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
			bookings = self.booking['passes']

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

	def calculate_all(self):
		pass

	def calculate(self):				# main function of this class, parses code of company and calculates charge
		if self.totalFare != -1 and self.baseFare != -1 and self.rules != 'Error' and self.taxes != [['Error']] and self.companyCode != 'Error':
			data = {'totalFare': self.totalFare, 'baseFare': self.baseFare, 'rules': self.rules, 	# necessary data
			'taxes': self.taxes, 'dates': self.__get_dates()}

			comp = None

			if self.companyCode == 'DV':	# Scat`s code
				from scat import Scat
				print("SCAT AirLine\n")
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
				return 'Change amount is ' + str(comp.calculate())

			except:
				return 'Error'
		else:
			return 'Error'