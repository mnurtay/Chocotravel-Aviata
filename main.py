from company import Company

def get_data(text):
		try:
			with open(text + '.json') as f:
				data = json.read(f)

			return data

		except:
			return None

def main():
	booking = get_data('booking')
	fare_rules = get_data('fare_rules')

	parser = parser(booking, fare_rules)

	msg = parser.calculate()
	
	print(msg)

if __name__ == '__main__':
	main()
