from Company import Company

def get_tarif(fare_rule_text):						# get tarif`s name from fare_rule_text
	words = fare_rule_text.split(' ')

	try:
		first_word = words[1].split('.')[2]			# get first_word of fare_rule_texxt
	except:
		first_word = ''

	if first_word == 'PERMITTED':					# 'Flexible' tarif`s text begins with 'PERMITTED'
		tarif = 'Flexible'

	elif first_word == 'CHANGES':					# other tarif`s text begins with 'CHANGES'
		try:										# try to define minutes
			minutes = int(words[4])
		except:
			minutes = 0

		try:										# try to define first_charge
			first_charge = int(words[11].split('\n')[0])
		except:
			first_charge = 0

		try:										# try to define second_charge
			second_charge = int(words[26])
		except:
			second_charge = 0

		print(minutes, first_charge, second_charge)

		if minutes != 0 and first_charge != 0 and second_charge != 0:	# define tarif by switch case
			tarif = switch_tarif(minutes, first_charge, second_charge)

		else:
			tarif = None
	else:
		tarif = None

	return tarif

def switch_tarif(minutes, first, second):			# get tarif`s name from minutes, first_charge and second_charge
	if minutes == 90:
		if first == 10 and second == 15:
			tarif = 'Bet/Economy'

		elif first == 15 and second == 20:
			tarif = 'Bet/Semi'

		elif first == 20 and second == 25:
			tarif = 'Bet/SStandart'

		elif first == 25 and second == 30: # except APROMO etc
			tarif = 'Bet/SPromo'

	elif minutes == 180:
		if first == 10 and second == 15:
			tarif = 'Int/Economy'

		elif first == 15 and second == 20:
			tarif = 'Int/Semi'

		elif first == 20 and second == 25:
			tarif = 'Int/SRestricted'

		elif first == 25 and second == 30: # except APROMO etc
			tarif = 'Int/SPromo'

	return tarif

def main():
	company = Company()

	msg = company.calculate()
	
	print(msg)

if __name__ == '__main__':
	main()
