
#!/usr/bin/env python
from core.acedb import AceDB
import time
import json
import os.path
from core.contracts import Contract

atomic = 100000000

def parse_config():
    """
    Parse the config.json file and return the result.
    """
    with open('config/config.json') as data_file:
        data = json.load(data_file)
        
    with open('config/networks.json') as network_file:
        network = json.load(network_file)
        
    with open('config/cryptoA.json') as A:
        cryptoA = json.load(A)
        
    with open('config/cryptoB.json') as B:
        cryptoB = json.load(B)
        
    return data, network, cryptoA, cryptoB

if __name__ == '__main__':
    
    # get config data
    data, network, A, B = parse_config()
    
    #listener listens from cryptoA
    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(A['dbusername'])
        # initalize sqldb object
        acesdb.setup()
    
    # check for new rewards accounts to initialize if any changed
    acesdb = AceDB(A['dbusername'])
    
    # get requested info for listener CURRENTLY HARDCODED FOR TESTING
    ts = int(time.time())
    send_address = "DS2YQzkSCW1wbTjbfFGVPzmgUe1tNFQstN"
    fee = data['flat_fee']
    send_amount = (1+fee) * atomic
    receive_addr = "DGExsNogZR7JFa2656ZFP9TMWJYJh5djzQ"
    receive_amount = 1 * atomic
    
    #insantiate new contract object
    c = Contract()
    c.create(ts, send_address, send_amount, receive_addr, receive_amount, fee)
    test = (c.contract,)
    acesdb.storeContracts(test)
    print("Contract Stored!")
