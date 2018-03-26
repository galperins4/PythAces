from flask import Flask, jsonify, json, request
from core.acedb import AceDB
from core.pythaces import Pythaces
from core.contracts import Contract
from core.conversion import Conversion
from pay import parse_config, get_network
import time
import os.path

atomic = 100000000

app = Flask(__name__)

@app.route("/")
#main landing page
def home():
    pass

@app.route("/coin", methods=['POST'])
def coin():
	# get send/receive addresses and amouunt
	print(request.json()
	send = request.args.get("send", type=str)
	recieve = request.args.get("receive", type=str)
       amount = request.args.get("amount", type=float)
        
        
        # do validations
        
        # calculate value
        
        #create contract
        '''
    c = Contract()
    c.create(ts, send_address, send_amount, receive_addr, receive_amount, total_fee)
    test = (c.contract,)
    acesdb.storeContracts(test)
    print("Contract Stored!")
    '''
    
    #return json to client (address, amount, vendorfield)
    return json.dumps(request.json)

#display all prices
@app.route("/prices")
def prices():
    
    try:
    	
    	conversion_rates = {} 
        # get conversion rates
        for key in coin:
        	cnv = Conversion(data['channel'], key)
        	conversion_rates[key] = cnv.conversion_rate()
        # get fees	
        feeDict = {
                "Flat fee": data['flat_fee'],
                "Percent fee": data['pct_fee']
                }
                
        priceDict = {
                "prices": conversion_rates,
                "fees": feeDict
                
        return jsonify(Prices=priceDict)
    
    except:
         error ={"Status":"Unsuccessful")
        return jsonify(Error=error)

#Change this to just send contracts
@app.route('/contracts') 
def contracts():
    pass

#get all capacity
@app.route("/capacity")
def capacity():
    try:
        service_availability = {}
    contracts = acesdb.unprocessedContracts()
    
    for key in coin:
        pythaces = Pythaces(fx_coins[key], atomic)
        # total capacity
        capacity = pythaces.service_capacity(coin[key]['service_acct'])
        # reserve capacity
        reserved = pythaces.reserve_capacity(contracts, coin[key]['addr_start'])
        #available capacity
        available = pythaces.available_capacity()
        
        service_availability[key] = {"Total Capacity": capacity,
                                    "Reserved Capacity": reserved,
                                    "Available Capcity": available}
        
        return jsonify(Capacity=service_availability)
    except:
    	error ={"Status":"Unsuccessful")
        return jsonify(Error=error)

if __name__ == "__main__":
    # get config data
    data, network, coin = parse_config()
    
    #listener listens from cryptoA
    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(data['dbusername'])
        # initalize sqldb object
        acesdb.setup()
    
    # check for new rewards accounts to initialize if any changed
    acesdb = AceDB(data['dbusername'])
    
    #initialize park objects for use
    fx_coins = {}
    for key in coin:
        fx_coins[key] = get_network(key, network, coin[key]['relay_ip'])
      
    app.run(host = data['channel_ip'], threaded=True)
