
#!/usr/bin/env python
from core.acedb import AceDB
from park.park import Park
# from liskbuilder.transaction import TransactionBuilder
# import random
import time
import json

def get_network(d, n, ip="localhost"):

    return Park(
        ip,
        n[d]['port'],
        n[d]['nethash'],
        n[d]['version']
    )

def parse_config():
    """
    Parse the config.json file and return the result.
    """
    with open('config/config.json') as data_file:
        data = json.load(data_file)
        
    with open('config/networks.json') as network_file:
        network = json.load(network_file)
        
    with open('config/coin.json') as coin_file:
        coin = json.load(coin_file)
        
    return data, network, coin

def get_passphrases(c):
    # Get the passphrase
    passphrase = coin[c]['service_account_passphrase']
    
    # Get the second passphrase
    secondphrase = coin[c]['service_account_secondphrase']
    if secondphrase == 'None':
        secondphrase = None

    return passphrase, secondphrase

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
def letter(l):
    for k,v in coin.items():
       if v.get("addr_start") == l:
           return k
    
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
    
    data, network, coin = parse_config()
    acedb = AceDB(data['dbusername'])
    reach = data['reach']
    
    fx_coins = {}
    for key in coin:
        fx_coins[key] = get_network(key, network, coin[key]['relay_ip'])
    
    '''
    if B['network'] in lisk_fork.keys():
        netname = lisk_fork[B['network']]
    '''
    while True:
        # get peers
        #signed_tx = []
        #unique_contracts = []
        
        # check for unprocessed payments
        if data['channel'] in lisk_fork.keys():
            pass
            #unprocessed_pay = acedb.stagedLiskPayment().fetchall()
        else:
            unprocessed_pay = acedb.stagedArkPayment().fetchall()

        # query not empty means unprocessed blocks
        if unprocessed_pay:
            
            for i in unprocessed_pay:
                if data['channel'] in lisk_fork.keys():
                    pass
                    #tx = TransactionBuilder().create(netname, i[2], i[3], passphrase, secondphrase)
                else:
                    # get first letter of send to address to find network
                    n_letter = i[2][0]
                    net = letter(n_letter)
                    print(net)
                    #instantiate park object
                    park = fx_coins[net]                    
                    # get passphrases
                    pp, sp = get_passphrases(net)
                    #send transaction - TO DO - NEED TO ADD PEER CAPABILITIES
                    transaction = park.transaction().create(i[2], str(i[3]), i[4], pp, sp)
                    print(transaction)
                    #transaction = park.transactions().create('address', 'amount', 'vendor', 'secret', 'second secret')
                    
                    #assuming transaction is good, update staged record for this contract
                    acedb.processStagedPayment(i[1])
                    
                    
                    #tx = park.transactionBuilder().create(i[2], str(i[3]), i[4], passphrase, secondphrase)
          
                #signed_tx.append(tx)
            
            # p = get_peers(park)
            
            #broadcast(signed_tx, p, park, reach)
            #acedb.processStagedPayment(i[1])

            # payment run complete
            print('Payment Run Completed!')
            #sleep 5 minutes between 50tx blasts
            time.sleep(300)
        
        else:
            time.sleep(300)
