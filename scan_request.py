import requests
import time
import random
import keys

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_hashes(contract,starting_block,key):

	response = requests.get('https://api.bscscan.com/api',
	    params={'module':'logs', 'action':'getLogs', 'fromBlock':starting_block, 
	    		'toBlock':'latest', 'address': contract,
	    		'apikey':key},
	    headers={}
	)


	results = response.json()['result']

	hashes = []
	for r in results:
		hashes.append(r['transactionHash'])

	# for h in hashes:
	# 	print(h)

	return(hashes)

def get_transaction_initiator_by(hash,key):

	response = requests.get('https://api.bscscan.com/api',
	    params={'module':'proxy', 'action':'eth_getTransactionByHash', 'txhash': hash, 
	    		'apikey':key},
	    headers={}
	)
	results = response
	# print(results.request.body)
	# print(results.request.url)
	# print(results.json()['result'])
	initiator = results.json()['result']['from']
	return(initiator)

def get_initiators(contract,starting_block,key):
	print('pulling log of hashes...')
	hashes = get_hashes(contract,starting_block,key)
	initiators = []
	i = 0
	print('pulling involved accounts from hashes on the blockchain...')
	printProgressBar(0, len(hashes)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for h in hashes:
		i += 1
		initiator = get_transaction_initiator_by(h,key)
		initiators.append(initiator)
		printProgressBar(i, len(hashes), prefix = 'Progress:', suffix = 'Complete', length = 50)
		time.sleep(0.2)


	newlist = []
	for i in initiators:
	  if i not in newlist:
	    newlist.append(i)

	initiators = newlist

	return(initiators)

def get_token_balance(contract,address,key):
	response = requests.get('https://api.bscscan.com/api',
	    params={'module':'account', 'action':'tokenbalance', 'contractaddress': contract,
	    		'address':address, 'tag':'latest',
	    		'apikey':key},
	    headers={}
	)
	token_balance = float(response.json()['result'])
	return(token_balance)




def get_holders_by_balance(contract,starting_block,min_balance,key):
	initiators = get_initiators(contract,starting_block,key)
	holders = []
	print('getting balances of accounts ...')
	printProgressBar(0, len(initiators)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
	iteration = 0
	for i in initiators:
		iteration += 1
		balance = get_token_balance(contract,i,key)
		if balance > min_balance:
			holders.append([i,balance])
		printProgressBar(iteration, len(initiators), prefix = 'Progress:', suffix = 'Complete', length = 50)
		time.sleep(.2)
	return(holders)

api_key = keys.api_key
contract = '0x9f66a7b29c123a1a4461bd1988d0aea0a3bb379b'
starting_block = '7645807'
min_balance = 10000

print('')
print('')

print('-----------------------------------')

print('WELCOME TO FIND A RANDOM WALLET BSC')

print('-----------------------------------')

print('')
print('')
print('Default options are: ')
print('')
print(f'contract: {contract}')
print(f'starting block: {starting_block}')
print(f'min_balance: {min_balance}')
print('')
print('-----------------------------------')
print('')

print('If you would like to change any of these options please type the option you would like to change.')
print('otherwise hit enter to proceed with the default options')

inp = input("type your response here: ")

while inp != '':
	if inp == 'contract':
		contract = input('input a new contract here: ')
	elif inp == 'starting block':
		starting_block = input('input a new starting block here: ')
	elif inp == 'min_balance':
		min_balance = input('input a new minimum balance here: ')
	else:
		print('that is not valid, try again')
	inp = input('type your next command here: ')

print('')
print('-----------------------------------')
print('')

holders = get_holders_by_balance(contract,starting_block,min_balance,api_key)
random.shuffle(holders)
winner = holders[0][0]

print('THE WINNER IS')
print(winner)

