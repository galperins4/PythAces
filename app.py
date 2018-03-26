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

@app.route("/<coin>")
def coin(coin):
    #


#display all prices
@app.route("/prices")
def prices():
    
    try:
        #pythaces class
        conv = Conversion()
        
        conversion_rate = conv.conversion_rate()
           
        priceDict = {
                "Address": A['service_acct'],
                "Conversion Rate":  conversion_rate,
                "Flat fee": data['flat_fee'],
                "Percent fee": data['pct_fee']
                }
    
    except:
        print("Error")
    

    return jsonify(Prices=priceDict)

#Change this to just send contracts
@app.route('/contracts', methods=['GET','POST']) 
def contracts():
    print(request.json)
    
    '''
    c = Contract()
    c.create(ts, send_address, send_amount, receive_addr, receive_amount, total_fee)
    test = (c.contract,)
    acesdb.storeContracts(test)
    print("Contract Stored!")
    '''
    
    return json.dumps(request.json)

#get all capacity
@app.route("/capacity")
def capacity():
    try:
        #pythaces class
        b = get_network(B, network, B['relay_ip'])
        pythaces = Pythaces(b, atomic)
    
        capacity = pythaces.service_capacity(B['service_acct'])
        
        #reserved_capacity = 
        contracts = acesdb.unprocessedContracts()
        reserved = pythaces.reserve_capacity(contracts)
    
        #available_capacity = 
        available = pythaces.available_capacity()
    
        capDict = {
                "Total Capacity": capacity,
                "Reserved Capacity": reserved,
                "Avaiable Capacity": available}
        
    except:
        print("Unsuccessful")
        
    return jsonify(Capacity=capDict)

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
    app.run(host = data['channel_ip'], threaded=True)
