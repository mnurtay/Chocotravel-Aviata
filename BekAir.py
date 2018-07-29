import xml.dom.minidom
import datetime

from company import Company

class BekAir():

	def __init__(self, fareRule_bekAir, totalFare, taxes):
		Company.__init__(self, fareRule_bekAir, totalFare, taxes)
		self.totalFare = int(totalFare)
		self.now = date[0] 
		self.departure = date[1] 

		self.mode = 'Error'
		self.charge_before = 3500
		self.charge_after = 4500

	def calculate(self):
		if get_status():
			non_ref = self.__calc_taxes()
			print(non_ref)

			if self.mode == 'BeforeDeparture':
				summa = self.totalFare - self.charge_before - non_ref
				return summa
			elif self.mode == 'AfterDeparture':
				summa = self.totalFare - self.charge_after - non_ref
				return summa

		return self.mode

	def get_status(self):
		if self.now < self.departure:
			self.mode = 'BeforeDeparture' 
		else:
			self.mode = 'AfterDeparture'
		return self.now < self.departure or self.departure > self.now

	def __calc_taxes(self):			
		non_ref = 0

		for tax in self.taxes:
			if tax[0] in self.non_ref:
				non_ref += int(tax[1])

		return non_ref

	def set_values(self):
		words = self.rules.split(' ')