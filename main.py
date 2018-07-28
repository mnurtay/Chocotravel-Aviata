from company import Company

def main():
	company = Company('booking', 'fare_rules')

	msg = company.calculate()
	
	print(msg)

if __name__ == '__main__':
	main()
