Welcome

This module uses the bscscan.com api to search the blockchain.
It pulls all transactions from a given block on the chain for a specific contract, finds all addresses that interacted with that contract, filters them by a minimum balance of tokens from the contract address, and then picks a random 'winner'.

To use this you will have to do two things:
Change the name of 'keys1.py' to simply 'keys.py'
add you BSCSCAN API into the 'keys.py' file.

To run the program, simply go into terminal, cd to this python program, and run:

python3 scan_request.py


The csv_random.py is a quicker version if you download the holders list as a csv from BscScan manually.