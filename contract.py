
#!/usr/bin/env python
from core.acedb import AceDB
from core.pythaces import Pythaces
from core.contracts import Contract
from pay import parse_config, get_network
import time
import os.path

atomic = 100000000



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
    
    #pythaces class
    bark = get_network(B, network, B['relay_ip'])
    pythaces = Pythaces(bark)
    capacity = pythaces.service_capacity(B['service_account'])
    print(capacity)
    
    #reserved_capacity = 
    contracts = acesdb.unprocessedContracts()
    reserved = pythaces.reserve_capacity(contracts)
    print(reserved)
    
    #available_capacity = 
    
    
    
    
    
    
    
    
