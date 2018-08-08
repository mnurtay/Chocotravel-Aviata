import json

from parsing import Parser
from converter import Converter

def get_json_data(text):
	try:
		with open(text + '.json', 'r') as f:
			data = json.load(f)
			
		return data

	except:
		return None

def write_data(data):
	with open('output.json', 'w') as f:
		json.dump(data, f, ensure_ascii=False)
		
	print('Success')

def main():
	bookings = get_json_data('fb200')['qwe']
	fare_rules = get_json_data('fr200')['qwe']

	# print(bookings)

	for booking in bookings:
		# print(booking)
		try:
			cid = booking['cid']

			is_valid = True

			fare = None

			for fare_rule in fare_rules:
				if fare_rule['combination_id'] == cid:
					fare = fare_rule
					break

			if fare == None:
				print('No match -> ' + str(cid))

			for q in json.loads(booking['js_ticket'])['passes']:
				# print('q')
				q['Routes'][0]['DepartureDate'] = "2019-08-09T04:00:00"

			parser = Parser(booking, fare)

			ress = parser.calculate_all()

			for res in ress:
				if res['data']['refunded_total'] == '':
					is_valid = False
					break

			if is_valid:
				print('Success -> ' + str(cid))

			else:
				print('Error -> ' + str(cid))

		except:
			print('Exception -> ' + str(cid))


if __name__ == '__main__':
	# main()

	c = Converter()

	print(c.calc('EUR', 1, 'KZT'))


