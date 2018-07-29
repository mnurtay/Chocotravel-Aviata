import xml.dom.minidom
import datetime

class Company:

	def __init__(self, file1, file2):
		self.booking = self.__get_xml_dom(file1)		# dom_object from booking.xml
		self.fareRule = self.__get_xml_dom(file2)		# dom_object from fare_rules.xml

		self.nameCompamy = self.__get_name()			# name of the air company
		self.totalFare = self.__get_total_fare()		# total fare of booking
		self.baseFare = self.__get_base_fare()			# base fare of booking
		self.rules = self.__get_rules()					# text of fare rules

		self.taxes = self.__get_taxes()					# array of pairs type of taxe and its amount

	def __get_name(self):			# get name of company
		return self.booking.getElementsByTagName("OperatingAirline")[1].firstChild.nodeValue

	def __get_total_fare(self):		# get total fare of booking
		return self.booking.getElementsByTagName("TotalFare")[2].firstChild.nodeValue

	def __get_base_fare(self):		# get base fare of booking
		return self.booking.getElementsByTagName("BaseFare")[1].attributes.item(0).value

	def __get_taxes(self):			# get array of pairs type of taxe and its amount
		taxes = self.booking.getElementsByTagName("Taxes")[1]
		
		listt = []
		
		for tax in taxes.childNodes:
			if tax.nodeType != tax.TEXT_NODE:
				arr = []
				arr.append(tax.childNodes[3].firstChild.nodeValue)
				arr.append(tax.childNodes[5].firstChild.nodeValue)
				listt.append(arr)

		return listt
		# for tax in taxes.childNodes:
		# print(tax.childNodes[0].nodeValue)

	def __get_xml_dom(self, file_name):		# get dom_object from xml_file
		xml_dom = xml.dom.minidom.parse(file_name + '.xml')
		xml_dom.normalize()

		return xml_dom

	def __get_dates(self):				# get current and departure date
		departureDate = self.booking.getElementsByTagName("DepartureDate")[0].firstChild.nodeValue
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

	def __get_rules(self):						# get fare_rule_text from fare_rules.xml dom_object
		subSection = self.fareRule.getElementsByTagName("SubSection")[5]
		paragraph = subSection.getElementsByTagName("Paragraph")[0]

		rules = paragraph.getElementsByTagName("Text")[0]

		return rules.firstChild.nodeValue

	def calculate(self):
		if self.nameCompamy == 'Scat Airlines':
			from scat import Scat

			comp = Scat(self.totalFare, self.baseFare, self.rules, self.taxes, self.__get_dates())

			return comp.calculate()

		elif self.nameCompamy == 'Qazaq Air':
			from qazaq import Qazaq

			comp = Qazaq(self.totalFare, self.baseFare, self.rules, self.taxes, self.__get_dates())

			return comp.calculate()

	