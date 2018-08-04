# class for currency exchange based on http://bankir.ru/kurs/valuta/

import requests
from bs4 import BeautifulSoup

class Converter:

	def __init__(self):
		self.main_link = 'http://bankir.ru'
		self.url = self.main_link + '/kurs/valuta'

		self.html = self.__get_html(self.url)

		self.parser = 'html.parser'

	def calc(self, first, amount, second):	# calculate exchange amount of first to second one
		self.first = first
		self.amount = amount
		self.second = second

		self.__first()
		self.__second()
		self.__third()

		return round(self.change, 2)

	def currencies(self):			# return list of available currencies
		bs = BeautifulSoup(self.html, self.parser)

		table = bs.find('table', class_ = 'kurs_reference_table')

		currencies = []

		currs = table.find_all('a', class_ = 'capitalize')

		for curr in currs:
			currencies.append(curr.get('title'))

		return currencies

	def __get_html(self, url):
		resp = requests.get(url)

		return resp.text

	def __first(self):
		bs = BeautifulSoup(self.html, self.parser)

		table = bs.find('table', class_ = 'kurs_reference_table')

		href = table.find('a', title = self.first).get('href')

		self.next_url = self.main_link + href

		self.next_html = self.__get_html(self.next_url)

		# print(self.next_url)

	def __second(self):
		bs = BeautifulSoup(self.next_html, self.parser)

		table = bs.find('table', class_ = 'kurs_reference_table')

		hrefs = table.select('td > a')

		for href in hrefs:

			if self.second in href.text:

				link = href.get('href')
				break

		self.next_next_url = self.main_link + link

		self.next_next_html = self.__get_html(self.next_next_url)

		# print(self.next_next_url)

	def __third(self):
		bs = BeautifulSoup(self.next_next_html, self.parser)

		table = bs.find('table', id = 'kurs_calc_tbl')

		self.coef = float(table.find('span', class_ = 'result_text_input').text.replace('\n', ''))

		values = table.find('span', class_ = 'ajax', id = 'calc_to').text.split(' ')

		self.num = 1

		for value in values:
			if self.__is_number(value):
				self.num = float(value)
				break

		self.change = self.num * self.coef * self.amount

	def __is_number(self, value):
		try:
			a = float(value)

			return True

		except:
			return False