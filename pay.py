
#!/usr/bin/env python
from core.acedb import AceDB
from park.park import Park
from liskbuilder.transaction import TransactionBuilder
# import random
from core.util import parse_config, get_network, get_passphrases, get_coin
import time
import json

'''
def get_peers(park):
    peers = []
    
    try:
        peers = park.peers().peers()['peers']
        print('peers:', len(peers))
    except BaseException:
    
    # fall back to delegate node to grab data needed
    bark = get_network(B, network, data['pay_relay_ip'])
    peers = bark.peers().peers()['peers']
    print('peers:', len(peers))
        
    return net_filter(peers)

def net_filter(p):
    peerfil= []
    # some peers from some reason don't report height, filter out to prevent errors
    for i in p:
        if "height" in i.keys():
            peerfil.append(i)
    
    #get max height        
    compare = max([i['height'] for i in peerfil]) 
    
    #filter on good peers for LISKcoins
    if B['network'] in lisk_fork.keys():
        f1 = list(filter(lambda x: x['version'] == network[B['network']]['version'], peerfil))
        f2 = list(filter(lambda x: x['state'] == 2, f1))
        final = list(filter(lambda x: compare - x['height'] < 153, f2))
        print('filtered peers', len(final))
    #filter on good peers for ARKcoins
    else:
        f1 = list(filter(lambda x: x['version'] == network[B['network']]['version'], peerfil))
        f2 = list(filter(lambda x: x['delay'] < 350, f1))
        f3 = list(filter(lambda x: x['status'] == 'OK', f2))
        final = list(filter(lambda x: compare - x['height'] < 153, f3))
        print('filtered peers', len(final))
        
    return final
'''

'''
def broadcast(tx, p, park, r):
    records = []
    # take peers and shuffle the order
    # check length of good peers
    if len(p) < r:  # this means there aren't enough peers compared to what we want to broadcast to
        # set peers to full list
        peer_cast = p
    else:
        # normal processing
        random.shuffle(p)
        peer_cast = p[0:r]

    #broadcast to localhost/relay first
    try:
        transaction = park.transport().createBatchTransaction(tx)
        records = [[j['vendorField'],j['recipientId'],j['amount'],j['id']] for j in tx]
        time.sleep(1)
    except BaseException:
    
    # fall back to delegate node to grab data needed
    bark = get_network(B, network, data['pay_relay_ip'])
    bark.transport().createBatchTransaction(tx)
    records = [[j['vendorField'],j['recipientId'],j['amount'],j['id']] for j in tx]
    time.sleep(1)
    
    acedb.storeTransactions(records)
    
     # rotate through peers and begin broadcasting:
    for i in peer_cast:
        ip = i['ip']
        peer_park = get_network(B, network, ip)
        # cycle through and broadcast each tx on each peer and save responses
        
        try:
            peer_park.transport().createBatchTransaction(tx)
            time.sleep(1)
        except:
            print("error")
'''        
if __name__ == '__main__':
   
    lisk_fork = {'oxy-t':'oxy', 
                'oxy': 'oxy', 
                'lwf-t': 'lwf', 
                'lwf': 'lwf', 
                'rise-t': 'rise', 
                'rise': 'rise', 
                'shift-t': 'shift', 
                'shift': 'shift',
                'onz-t': 'onz',
                'onz': 'onz',
                'lisk-t': 'lisk',
                'lisk' : 'lisk'}
    
    network, coin = parse_config()
    acedb = AceDB(coin['channel']['dbusername'])
    reach = coin['channel']['reach']
    
    fx_coins = {}
    for key in coin:
        if key != "channel":
            fx_coins[key] = get_network(key, network, coin[key]['relay_ip'])
    
    while True:
        
        # check for unprocessed payments 
        unprocessed_pay = acedb.stagedArkPayment().fetchall()

        # query not empty means unprocessed blocks
        if unprocessed_pay:            
            for i in unprocessed_pay:
                signed_tx=[]
                # get first letter and find network
                net = get_coin(i[2], coin)
                #instantiate park object 
                park = fx_coins[net]                    
                # get passphrases
                pp, sp = get_passphrases(net, coin)
                
                if net in lisk_fork.keys():
                    netname = lisk_fork[net]
                    try:
                        tx = TransactionBuilder().create(netname, i[2], i[3], pp, sp)
                        record = [[i[4],tx['recipientId'],tx['amount'],tx['id']]]
                        signed_tx.append(tx)
                        transaction = park.transport().createBatchTransaction(signed_tx)
                    
                        #assuming transaction is good, update staged record for this contract
                        acedb.processStagedPayment(i[1])
                        acedb.storeTransactions(record)
                    except:
                         print("Error Sending Transaction, Try again!")
      
                else:
                    
                    #send transaction - TO DO - NEED TO ADD PEER CAPABILITIES
                    try:
                        tx = park.transactionBuilder().create(i[2], str(i[3]), i[4], pp, sp)
                        record = [[i[4],tx['recipientId'],tx['amount'],tx['id']]]
                        signed_tx.append(tx)
                        transaction = park.transport().createBatchTransaction(signed_tx)
                    
                        #assuming transaction is good, update staged record for this contract
                        acedb.processStagedPayment(i[1])
                        acedb.storeTransactions(record)
                    except:
                        print("Error Sending Transaction, Try again!")

            # payment run complete 
            print('Payment Run Completed!')
            #sleep 5 minutes between 50tx blasts
            time.sleep(60)
        
        else:
            time.sleep(60)
