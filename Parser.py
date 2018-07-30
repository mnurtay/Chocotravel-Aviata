import datetime
import json

class Parser:

	def __init__(self, booking, fare_rules):
		self.booking = json.loads(booking['js_ticket'])
		self.fareRule = json.loads(fare_rules['tarif_xml'])

		self.companyCode = self.__get_code()
		self.totalFare = self.__get_total_fare()
		self.taxes = self.__get_taxes()
		self.baseFare = self.__get_base_fare()

		self.rules = self.__get_rules()

	def __get_code(self):			# get code of airline company
		try:
			companyCode = self.booking['passes'][0]['Routes'][0]['OperatingAirlineCode']

			# print(companyCode)

			return companyCode

		except:
			return 'Error'			# return exception as string 'Error'

	def __get_total_fare(self):		# get total fare of booking
		try:
			totalFare = int(self.booking['passes'][0]['TotalFare'])

			# print(totalFare)

			return totalFare

		except:
			return -1				# return exception as -1

	def __get_taxes(self):			# get taxes as array of arrays of its type and amount
		try:
			taxes = self.booking['passes'][0]['Taxes']
			values = []

			for tax in taxes:
				value = []

				value.append(tax['CountryCode'])
				value.append(tax['Amount'])

				values.append(value)

			# print(values)

			return values

		except:
			return [['Error']]		# return exception as [['Error']]

	def __get_base_fare(self):		# calculating base fare according to total fare and taxes
		try:
			if self.totalFare != -1:
				baseFare = self.totalFare

				for tax in self.taxes:
					baseFare -= int(tax[1])

				# print(baseFare)

				return baseFare

			else: return -1

		except:
			return -1				# return exception as -1


	def __get_rules(self):			# get text of rules for penalties
		try:
			rules = self.fareRule['rules'][0]
			text = ''

			for rule in rules:
				if rule['rule_title'] == 'PENALTIES':
					text += rule['rule_text']

			text = text.replace('       ', '').replace('      ', '').replace('     ', '')
			text = text.replace('    ', '').replace('   ', '').replace('  ', '')
			text = text.replace(' <br>', '')

			# print(text)

			return text

		except:
			return 'Error'			# return exception as string 'Error'

	def __get_dates(self):			# get current and departure date
		departureDate = self.booking['passes'][0]['Routes'][0]['DepartureDate']
		currentDate = datetime.datetime.now().isoformat()

		# split string
		departureDate = departureDate.split("T", 1)
		currentDate = currentDate.split("T", 1)
		currentDate[1] = currentDate[1].split(".", 1)[0]

		# castDate
		departureDate = self.__cast_date(departureDate)
		currentDate = self.__cast_date(currentDate)

		return currentDate, departureDate

	def __cast_date(self, data):	# auxillary function for dates
		date = data[0].split("-", 2)
		time = data[1].split(":", 2)
		date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 
			int(time[0]), int(time[1]), int(time[2]))

		return date

	def calculate(self):				# main function of this class, parses code of company and calculates charge
		if self.totalFare != -1 and self.baseFare != -1 and self.rules != 'Error' and self.taxes != [['Error']] and self.companyCode != 'Error':
			data = {'totalFare': self.totalFare, 'baseFare': self.baseFare, 'rules': self.rules, 	# necessary data
			'taxes': self.taxes, 'dates': self.__get_dates()}
			if self.companyCode == 'DV':	# Scat`s code
				from scat import Scat
				print("SCAT AirLine\n")
				comp = Scat(data)

				return 'Change amount is ' + str(comp.calculate())

			elif self.companyCode == "SU":
				from aeroflot import Aeroflot
				print("Aeroflot AirLine\n")
				comp = Aeroflot(data)

				return comp.calculate()

			elif self.companyCode ==  "Z9": 
				from BekAir import BekAir
				print("Bek Air AirLine\n")
				comp = BekAir(data)

				return 'Change amount is ' + str(comp.calculate())

		else:
			return 'Error'