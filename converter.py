# class for currency exchange based on http://bankir.ru/kurs/valuta/

import requests

from bs4 import BeautifulSoup

class Converter:

	def __init__(self):
		url = "https://prodengi.kz/currency/"
		html = self.__get_html(url)
		self.bs = BeautifulSoup(html, 'html.parser')

	def calc(self, first, amount, second):	# calculate exchange amount of first to second one
		if second == "KZT":
			return round(self.__first(first, amount), 2)
		else:
			return round(self.__second(first, amount, second), 2)

	def __first(self, first, amount):
		price = self.bs.celect('.content_list .'+first+' .price_buy')
		return float(price[0].getText()) * float(amount)
	
	def __second(self, first, amount, second):
		temp_price = self.bs.celect('.content_list .'+first+' .price_buy')
		temp_price = float(temp_price) * float(amount)
		temp_price_2 = self.bs.celect('.content_list .'+second+' .price_buy')
		temp_price_2 = 1 / float(temp_price_2)
		return temp_price * temp_price_2

	def currencies(self):			# return list of available currencies
		currs = self.bs.select('.denomination .short_name')
		currencies = []

		for curr in currs:
			currencies.append(curr.getText())
		return currencies

	def __get_html(self, url):
		resp = requests.get(url)
		
		return resp.text


	def __is_number(self, value):
		try:
			a = float(value)
			return True
		except:
			return False