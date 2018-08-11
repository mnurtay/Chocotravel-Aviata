import json

from datetime import datetime
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
	with open('outputs.json', 'w') as f:
		json.dump(data, f, ensure_ascii=False)
		
	#print('Success')

def main():
	first = datetime.now()

	bookings = get_json_data('test_b')['list']
	fare_rules = get_json_data('test_f')['list']

	# print(bookings)

	

	data = []

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

			if fare == None or fare == '':
				#print('No match -> ' + str(cid))

				dt = {'test': 'No match'}

				data.append(dt)

				continue

			parser = Parser(booking, fare)

			ress = parser.calculate_all()

			# print(ress)

			for res in ress:
				if res['data']['refunded_total'] == 'NA':
					is_valid = False
					break


			if is_valid:
				#print('Success -> ' + str(cid))

				main_data = []

				main_data.append(ress)

				dt = {'test': main_data}

				data.append(dt)

				continue

			else:
				#print('Error -> ' + str(cid))

				dt = {'test': 'Error'}

				data.append(dt)

				continue

		except:
			#print('Exception -> ' + str(cid))

			dt = {'test': 'Exception'}

			data.append(dt)

			continue

	qwe = {'list': data}

	write_data(qwe)

	second = datetime.now()
	print("it only took", second - first, "seconds")
	

if __name__ == '__main__':
	main()