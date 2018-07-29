import xml.dom.minidom

class BekAir():

	def __init__(self, rules, totalFare,baseFare, taxes, dates):
		self.totalFare = int(totalFare)
		self.baseFare = int(baseFare)
		self.rule = rules
		self.taxes = taxes
		self.dates = dates

		self.mode = ' '
		self.check = 0
		self.now = dates[0]
		self.depDate = dates[1]
		self.charge_before = 3500
		self.charge_after = 4500

	def calculate(self):
		if __get_status():

			if self.mode == 'BeforeDep':
				return self.totalFare - self.charge_before
	
			elif self.mode == 'Afterdep':
				return self.totalFare - self.charge_after
		return 'Error'

	def __get_status(self):
		if self.now < self.depDate:
			self.mode = 'BeforeDep'
		else:
			self.mode = 'Afterdep'

		return self.now < self.depDate or self.depDate > self.now

	def __set_values(self):
		words = self.rules.split('\n')

		for rule in words:
			if 'PENALTIES' in rule:
				self.check = 1
				pass