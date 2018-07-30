import json
from parser import Parser

def get_data(text):
	try:
		with open(text + '.json') as f:
			data = json.load(f)

		return data

	except:
		return None

def write_data(data):
	with open('output.json', 'a') as f:
		for dt in data:
			json.dump(dt, f, ensure_ascii=False)


	print('Success')

def main():
	booking = get_data('booking')
	fare_rules = get_data('fare_rules')

	parser = Parser(booking, fare_rules)

	data = parser.calculate_all()

	print(data)
	
	write_data(data)

if __name__ == '__main__':
	main()
