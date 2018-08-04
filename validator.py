# class fov validating numbers, percent signs and currencies

from converter import Converter

class Validator:
	
	def __init__(self):
		self.c = Converter()

		self.currencies = self.c.currencies()

		self.percents = ['PERCENT', 'PCT', '%', 'PERCENTS']

	def is_percent(self, text):
		if text in self.percents:
			return True

		return False

	def is_number(self, text):
		try:
			a = float(text)

			# print(a)

			return True

		except:
			return False

	def is_currency(self, text):
		if text in self.currencies:
			return True

		return False