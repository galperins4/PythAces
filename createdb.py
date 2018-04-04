from pay import parse_config
from core.acedb import AceDB

if name 

# get config data
    data, network, coin = parse_config()
    
    #listener listens from cryptoA
    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(data['dbusername'])
        # initalize sqldb object
        acesdb.setup()
