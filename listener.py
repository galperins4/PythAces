#!/usr/bin/env python

from db.psql import DB
from db.acedb import AceDB
import time
import json

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
    
def get_dbname():
    ark_fork = ['ark','dark','kapu']
    if  data['network_a'] in ark_fork:
        uname = data['dbusername']
    else:
        uname = network[data['network_a']]['db_user']
        
    return uname

if __name__ == '__main__':
    
    # get config data
    data, network = parse_config()

    # initialize db connection
    #check for special usernames needed for lisk forks
    username = get_dbname()
    db = DB(network[data['network_a']]['db'], username, network[data['network_a']]['db_pw'])
    
    # connect to contracts database
    acesdb = AceDB(data['dbusername'])
    
    # processing loop
    while True:
        #look for unprocessed contracts
        unprocessed = acesdb.unprocessedContracts().fetchall()
          
        # query not empty means unprocessed contracts
        if unprocessed:
            listen_start = int(time.time()) - data['network_a_epoch']
            print("initial ts:", listen_start)
            for c in unprocessed:
                #listen_start = c[1]-data['network_a_epoch']
                transactions = db.listen_transactions(listen_start)
                print("# of tx to process:", len(transactions))
                
                if transactions:
                    for tx in transactions:
                        #check if contract matches vendor field
                        if c[0] == tx[4]:
                            #we have a match - mark as processed and move to staging
                            #store payment
                            msg = "Thanks for using PythAces"
                            acesdb.storePayment(c[0], c[4], c[5], msg)
                        
                            #mark as processed
                            acesdb.markAsProcessed(c[0])
                        else:
                            pass
                    #update list_start based on last timestamp
                    print(transactions[-1])
                    listen_start = transactions[-1][1]
                    print("updated ts:", listen_start)
                    #update transactions to break loop
                    transactions = []
                else:
                    print("No Transactions to Process")
                
                #wait 60 seconds and then grab another set of transactions
                time.sleep(60)
                
        #no unprocessed contract
        print("No unprocessed contracts, sleeping for 60 seconds")
        time.sleep(60)
