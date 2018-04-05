#!/usr/bin/env python
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
        
    with open('config/networks.json') as network_file:
        network = json.load(network_file)
        
    with open('config/coin.json') as coin_file:
        coin = json.load(coin_file)
        
    return network, coin

def get_passphrases(c):
    # Get the passphrase
    passphrase = coin[c]['service_account_passphrase']
    
    # Get the second passphrase
    secondphrase = coin[c]['service_account_secondphrase']
    if secondphrase == 'None':
        secondphrase = None

    return passphrase, secondphrase
