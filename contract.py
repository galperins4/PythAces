
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
    data, network, coin = parse_config()

    # check to see if db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(data['dbusername'])
        # initalize sqldb object
        acesdb.setup()
    
    # check for new rewards accounts to initialize if any changed
    acesdb = AceDB(data['dbusername'])
    
    #Get capacity stats
    #pythaces class - need list of eligable coins for parks
    
    fx_coins = {}
    for key in coin:
        fx_coins[key] = get_network(key, network, coin[key]['relay_ip'])
    
    print(fx_coins)
    
    service_availability = {}
    contracts = acesdb.unprocessedContracts()
    
    for key in coin:
        pythaces = Pythaces(fx_coins[key], atomic)
        # total capacity
        capacity = pythaces.service_capacity(coin[key]['service_acct'])
        # reserve capacity
        reserved = pythaces.reserve_capacity(contracts, coin[key]['addr_start'])
        #available capacity
        available = pythaces.available_capacity()
        
        service_availability[key] = {"Total Capacity": capacity,
                                    "Reserved Capacity": reserved,
                                    "Available Capcity": available}
    
    print(service_availability)
    
    conversion_rates = {}
    for key in coin:
        conversion_rates[key] = pythaces.conversion_rate(data['channel'], key)
    
    print(conversion_rates)

    # get requested info for listener CURRENTLY HARDCODED FOR TESTING
    ts = int(time.time())
    receive_addr = "DGExsNogZR7JFa2656ZFP9TMWJYJh5djzQ"
    receive_amount = 250 * atomic
    print(receive_amount)
    
    send_address = "DS2YQzkSCW1wbTjbfFGVPzmgUe1tNFQstN"
    # send_amt = 250
    converted_amount = receive_amount * conversion_rates['kapu']
    f_fee = data['flat_fee'] * atomic
    p_fee = data['pct_fee'] * converted_amount
    total_fee = int((p_fee + f_fee))
    print(total_fee)
    
    
    send_amount = int((converted_amount)) + total_fee
    print(send_amount)
    
    #insantiate new contract object
    c = Contract()
    c.create(ts, send_address, send_amount, receive_addr, receive_amount, total_fee)
    test = (c.contract,)
    acesdb.storeContracts(test)
    print("Contract Stored!")
    
    
    
    
    
    
    
    
    
