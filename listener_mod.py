#!/usr/bin/env python

from core.psql import DB
from core.acedb import AceDB
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
        
    with open('config/cryptoA.json') as A:
        cryptoA = json.load(A)
        
    with open('config/cryptoB.json') as B:
        cryptoB = json.load(B)
      
    with open('config/coin.json') as coin:
        cryptoB = json.load(coin)
        
    return data, network, cryptoA, cryptoB, coin
 
def get_dbname():
    ark_fork = ['ark','dark','kapu', 'dkapu', 'persona-t']
    if  A['network'] in ark_fork:
        uname = A['dbusername']
    else:
        uname = network[A['network']]['db_user']
        
    return uname

if __name__ == '__main__':
    
    # get config data
    data, network, A, B, coin = parse_config()

    # initialize db connection
    #check for special usernames needed for lisk forks
    username = get_dbname()
    db = DB(network[A['network']]['db'], username, network[A['network']]['db_pw'])
    ''' 
    # connect to contracts database and get last row of tx
    acesdb = AceDB(A['dbusername'])
    '''
    check_start = None
    '''
    check_start = acesdb.getRows().fetchall()
    '''
    if check_start:
        #this means we have a starting row
        for r in check_start:
            r_start = r[0]
        #set starting row for processing
        start_row = r_start
    else:
        #no starting transaction processed      
        sr = db.last_transaction()
        start_row = sr[0][0]
        #store starting row
        acesdb.storeRow(start_row)
    
    # processing loop
    while True:
        '''
        #look for unprocessed contracts
        unprocessed = acesdb.unprocessedContracts().fetchall()
        print("Count of unprocessed contracts:", len(unprocessed))
          
        # query not empty means unprocessed contracts
        if unprocessed:
            expire = int(time.time())
        '''
        
        transactions = db.listen_transactions(start_row)
        tx_cnt =  len(transactions)
            
        '''    for c in unprocessed:
                #expire contracts after 15 minutes
                if (expire - c[1]) > 900 :
                    acesdb.expireContract(c[0])
           '''     
        if transactions:
            for tx in transactions:
            net_check = tx[5].split(":")
            if net_check[0] in coin.keys() and coin['dark']['service_acct'] == tx[2];
                #possible match
                receive_net = net_check[0]:
                
                #look for match - added error handling for index issues
                try:
                    if len(net_check[1] == 34:
                    #high likelihood of match
                    #DO SOME CALCULATIONS HERE TO FIGURE OUT FEES AND RECEIVE AMOUNTS
                    
                    msg = "Aces Test"       
                    
                    acesdb.storePayment(tx[5], net_check[1], atomic, msg)
                    #acesdb.markAsProcessed(c[0])
            
            start_row += tx_cnt
            print("Processed through row:", start_row)
            
            #update start_row in database
            #acesdb.updateRow(start_row)
            
        print("Waiting 60 seconds for new transactions")
        time.sleep(60)
