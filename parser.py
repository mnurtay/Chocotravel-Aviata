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


	def __get_code(self):
		try:
			return self.booking['passes'][0]['Routes'][0]['OperatingAirlineCode']

		except:
			return 'Error'

	def __get_total_fare(self):
		try:
			return self.booking['passes'][0]['TotalFare']

		except:
			return -1

	def __get_taxes(self):
		try:
			taxes = self.booking['passes'][0]['Taxes']
			values = []

			for tax in taxes:
				value = []

				value.append(tax['CountryCode'])
				value.append(tax['Amount'])

				values.append(value)

			return values

		except:
			return [['Error']]

	def __get_base_fare(self):
		try:
			if self.totalFare != -1:
				baseFare = self.totalFare

				for tax in self.taxes:
					baseFare -= tax[1]

				return baseFare

			else: return -1

		except:
			return -1


	def __get_rules(self):
		try:
			rules = self.fareRule['rules'][0]
			text = ''

			for rule in rules:
				if rule['rule_title'] == 'PENALTIES':
					text += rule['rule_text']

			text = text.replace('       ', '').replace('      ', '').replace('     ', '')
			text = text.replace('    ', '').replace('   ', '').replace('  ', '')
			text = text.replace(' <br>', '')

			return text

		except:
			return 'Error'

	def __get_dates(self):				# get current and departure date
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

	def __cast_date(self, data):
		date = data[0].split("-", 2)
		time = data[1].split(":", 2)
		date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 
			int(time[0]), int(time[1]), int(time[2]))

		return date

	def calculate(self):
		if self.companyCode == 'DV':	# Scat`s code
			from scat import Scat

			comp = Scat(self.totalFare, self.baseFare, self.rules, self.taxes, self.__get_dates())

			return comp.calculate()

		elif self.companyCode == 'Z9':
			from qazaq import Qazaq

			comp = Qazaq(self.totalFare, self.baseFare, self.rules, self.taxes, self.__get_dates())


			return comp.calculate()
