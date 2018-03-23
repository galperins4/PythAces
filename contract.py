
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
    
    #Get capacity stats
    #pythaces class
    coina = get_network(A, network, A['relay_ip'])
    coinb = get_network(B, network, B['relay_ip'])
    
    pythaces = Pythaces(coinb, atomic)
    capacity = pythaces.service_capacity(B['service_acct'])
    print("Total Capacity: ", capacity)
    
    #reserved_capacity = 
    contracts = acesdb.unprocessedContracts()
    reserved = pythaces.reserve_capacity(contracts)
    print("Reserved Capacity: ", reserved)
    
    #available_capacity = 
    available = pythaces.available_capacity()
    print("Available Capcity: ", available)
    
    conversion_rate = pythaces.conversion_rate()
    print(conversion_rate)
    
    # get requested info for listener CURRENTLY HARDCODED FOR TESTING
    ts = int(time.time())
    receive_addr = "DGExsNogZR7JFa2656ZFP9TMWJYJh5djzQ"
    receive_amount = 1 * atomic
    print(receive_amount)
    
    send_address = "DS2YQzkSCW1wbTjbfFGVPzmgUe1tNFQstN"
    # send_amt = 250
    converted_amount = receive_amount * conversion_rate
    f_fee = data['flat_fee']
    p_fee = data['pct_fee'] * converted_amount
    total_fee = (p_fee + f_fee) * atomic
    
    send_amount = (converted_amount * atomic) + total_fee
    print(send_amount)
    
    #insantiate new contract object
    c = Contract()
    c.create(ts, send_address, send_amount, receive_addr, receive_amount, total_fee)
    test = (c.contract,)
    acesdb.storeContracts(test)
    print("Contract Stored!")
    
    
    
    
    
    
    
    
    
