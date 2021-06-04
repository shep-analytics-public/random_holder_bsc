import csv
import random

min_seg_balance = 5000000

file = open("tokenholders.csv", "r")
csv_reader = csv.reader(file)

lists_from_csv = []
for row in csv_reader:
    lists_from_csv.append(row)

big_enough_wallet_addresses = []

for holder in lists_from_csv:
	if holder[1] != 'Balance' and float(holder[1]) > min_seg_balance:
		#wallet is big enough		
		big_enough_wallet_addresses.append(holder[0])
	else:
		#not big enough
		pass

random.shuffle(big_enough_wallet_addresses)

print('lucky winner is')
print(big_enough_wallet_addresses[0])