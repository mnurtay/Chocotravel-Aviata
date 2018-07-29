import xml.dom.minidom

class BekAir():

	def __init__(self, fareRule_bekAir, totalFare,baseFare, taxes, dates):
		self.totalFare = int(totalFare)
		self.baseFare = int(baseFare)
		self.fareRule_bekAir = fareRule_bekAir
		self.taxes = taxes
		self.dates = dates

		self.check = 0
		self.now = dates[0]
		self.depDate = dates[1]
		self.charge_before = 3500
		self.charge_after = 4500

	def calculate(self):
		#еще не дописал
			

	def __get_status(self):
		return self.now < self.depDate

	def __set_values(self):
		words = self.rules.split(' ')
		for rule in words:
			if 'PENALTIES' in rule:
				self.check = 1
				