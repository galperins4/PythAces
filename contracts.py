#!/usr/bin/env python
from db.acedb import AceDB
import time
import json
import os.path
from uuid import uuid4

atomic = 100000000

def parse_config():
    """
    Parse the config.json file and return the result.
    """
    with open('config/config.json') as data_file:
        data = json.load(data_file)

    with open('config/networks.json') as network_file:
        network = json.load(network_file)

    return data, network

if __name__ == '__main__':

    # get config data
    data, network = parse_config()

    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:
        acesdb = AceDB(data['dbusername'])
        # initalize sqldb object
        acesdb.setup()

    # check for new rewards accounts to initialize if any changed
    acesdb = AceDB(data['dbusername'])

    # get requested info for listener CURRENTLY HARDCODED FOR TESTING
    contract = str(uuid4())
    ts = int(time.time())
    send_address = "DS2YQzkSCW1wbTjbfFGVPzmgUe1tNFQstN"
    fee = data['flat_fee']
    send_amount = (1+fee) * atomic
    receive_addr = "DGExsNogZR7JFa2656ZFP9TMWJYJh5djzQ"
    receive_amount = 1 * atomic


    # get input from front end
    # currently will do manually until front end is built for testing
    new_contract = ((contract, ts, send_address, send_amount, receive_addr, receive_amount, fee),)
    acesdb.storeContracts(new_contract)
    print("Contract Stored!")
