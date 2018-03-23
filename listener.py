#!/usr/bin/env python

from core.psql import DB
from core.acedb import AceDB
import time
from contract import parse_config

atomic = 100000000
 
def get_dbname():
    ark_fork = ['ark','dark','kapu']
    if  A['network'] in ark_fork:
        uname = A['dbusername']
    else:
        uname = network[A['network']]['db_user']
        
    return uname

if __name__ == '__main__':
    
    # get config data
    data, network, A, B = parse_config()

    # initialize db connection
    #check for special usernames needed for lisk forks
    username = get_dbname()
    db = DB(network[A['network']]['db'], username, network[A['network']]['db_pw'])
    sr = db.last_transaction()
    start_row = sr[0][0]
    
    # connect to contracts database and get last row of tx
    acesdb = AceDB(A['dbusername'])
    
    # processing loop
    while True:
        #look for unprocessed contracts
        unprocessed = acesdb.unprocessedContracts().fetchall()
        print("Count of unprocessed contracts:", len(unprocessed))
          
        # query not empty means unprocessed contracts
        if unprocessed:
            expire = int(time.time())
            print("Processed through row:", start_row) 
            transactions = db.listen_transactions(start_row)
            tx_cnt =  len(transactions)
            
            for c in unprocessed:
                #expire contracts after 15 minutes
                if (expire - c[1]) > 900 :
                    acesdb.expireContract(c[0])
                
                elif transactions:
                    for tx in transactions:
                        #note t[0] is tx
                        #check if contract matches vendor field
                        if c[0] == tx[5] and c[2] == tx[1] and A["service_acct"] == tx[2] and c[3] == tx[3]:
                            #we have a match - mark as processed and move to staging
                            #store payment and mark as processed
                            msg = "Thanks for using PythAces - contract "+c[0]
                            acesdb.storePayment(c[0], c[4], c[5], msg)
                            acesdb.markAsProcessed(c[0])
            #increment rows processed
            start_row += tx_cnt
            print("Processed through row:", start_row)

        print("Waiting 60 seconds for new transactions")
        time.sleep(60)
