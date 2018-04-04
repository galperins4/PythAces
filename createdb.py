from pay import parse_config
from core.acedb import AceDB
import os.path

if __name__ == "__main__":

# get config data
    network, coin = parse_config()
    
    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(coin['channel']['dbusername'])
        # initalize sqldb object
        acesdb.setup()
