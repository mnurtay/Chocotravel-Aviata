import datetime
import json

class Parser:

	def __init__(self, booking, fare_rules):
		self.booking = json.loads(booking['js_ticket'])
		self.fareRule = json.loads(fare_rules['tarif_xml'])

		self.companyCode = self.__get_code()
		self.totalFare = self.__get_fare()
		self.taxes = self.__get_taxes()

		self.rules = self.__get_rules()


	def __get_code(self):
		try:
			return self.booking['passes'][0]['Routes'][0]['OperatingAirlineCode']

		except:
			return 'Error'

	def __get_fare(self):
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

	def __get_rules(self):
		try:
			rules = self.fareRule['rules'][0]
			text = ''

			for rule in rules:
				if rule['rule_title'] == 'PENALTIES':
					text += rule['rule_text']

			text = text.replace('       ', '').replace('      ', '').replace('     ', '')
			text = text.replace('    ', '').replace('   ', '').replace('  ', '')

			return text

		except:
			return 'Error'