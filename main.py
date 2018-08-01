import json
from parsing import Parser

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
	booking = get_json_data('booking')
	fare_rules = get_json_data('fare_rules')

	if booking != None and fare_rules != None:
		parser = Parser(booking, fare_rules)

		data = parser.calculate_all()

		# print(data)
	
		write_data(data)

	else:
		print({'Error': 'Error'})

		write_data({'Error': 'Error'})

if __name__ == '__main__':
	main()
