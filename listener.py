#!/usr/bin/env python

from core.psql import DB
from core.acedb import AceDB
import time
from core.util import parse_config, is_ark_fork, get_dbname

atomic = 100000000

if __name__ == '__main__':
    
    #ark_fork = ['ark','dark','kapu', 'dkapu', 'persona-t']
    # get config data
    network, coin = parse_config()

    # initialize db connection
    #check for special usernames needed for lisk forks
    username = get_dbname()
    db = DB(network[coin['channel']['channel']]['db'], username, network[coin['channel']['channel']]['db_pw'])
 
    # connect to contracts database and get last row of tx
    acesdb = AceDB(coin['channel']['dbusername'])
    
    check_start = acesdb.getRows().fetchall()
    
    if check_start:
        #this means we have a starting row
        for r in check_start:
            r_start = r[0]
        #set starting row for processing
        start_row = r_start
    else:
        #no starting transaction processed      
        if  is_ark_fork(coin['channel']['channel']): 
            sr = db.last_transaction()
        else:
            sr = db.last_transaction_lisk()
        start_row = sr[0][0]
        #store starting row
        acesdb.storeRow(start_row)
    
    # processing loop
    while True:
        #look for unprocessed contracts
        unprocessed = acesdb.unprocessedContracts().fetchall()
        print("Count of unprocessed contracts:", len(unprocessed))
          
        # query not empty means unprocessed contracts
        if unprocessed:
            expire = int(time.time())
            if is_ark_fork(coin['channel']['channel']):
                transactions = db.listen_transactions(start_row)
            else:
                transactions = db.listen_transactions_lisk(start_row)
            tx_cnt =  len(transactions)
            
            for c in unprocessed:
                #expire contracts after 15 minutes
                if (expire - c[1]) > 900 :
                    acesdb.expireContract(c[0])
                
                elif transactions:
                    for tx in transactions:
                        #note t[0] is tx
                        #check if contract matches vendor field
                        #vendor field dpos
                        if  is_ark_fork(coin['channel']['channel']):
                            if c[0] == tx[5] and c[2] == tx[1] and coin['channel']["service_acct"] == tx[2] and c[3] == tx[3]:
                                #we have a match - mark as processed and move to staging
                                #store payment and mark as processed
                                msg = "Pythaces contract-"+c[0]
                                acesdb.storePayment(c[0], c[4], c[5], msg)
                                acesdb.markAsProcessed(c[0])
                        #non vendor field dpos 
                        else: 
                            if c[2] == tx[1] and coin['channel']["service_acct"] == tx[2] and c[3] == tx[3]:
                                msg = "Pythaces contract-"+c[0]
                                acesdb.storePayment(c[0], c[4], c[5], msg)
                                acesdb.markAsProcessed(c[0])
            #increment rows processed
            start_row += tx_cnt
            print("Processed through row:", start_row)
            #update start_row in database
            acesdb.updateRow(start_row)

        print("Waiting 60 seconds for new transactions")
        time.sleep(60)
