from flask import Flask, jsonify, json, request
from core.acedb import AceDB
from core.pythaces import Pythaces
from core.contracts import Contract
from pay import parse_config, get_network
import time
import os.path
atomic = 100000000

app = Flask(__name__)

@app.route("/prices")
def prices():
    return "Return Employee JSON data"

@app.route('/contracts', methods=['POST']) 
def contracts():
    print(request.json)
    return json.dumps(request.json)

@app.route("/capacity")
def capacity():
    try:
        
        #a = get_network(A, network, A['relay_ip'])
        b = get_network(B, network, B['relay_ip'])
    
        pythaces = Pythaces(b, atomic)
        capacity = pythaces.service_capacity(B['service_acct'])
        print("Total Capacity: ", capacity)
    
        #reserved_capacity = 
        contracts = acesdb.unprocessedContracts()
        reserved = pythaces.reserve_capacity(contracts)
        print("Reserved Capacity: ", reserved)
    
        #available_capacity = 
        available = pythaces.available_capacity()
        print("Available Capacity: ", available)
    
        capDict = {
                "Total Capacity": capacity,
                "Reserved Capacity": reserved,
                "Avaiable Capacity": available}
        
        #convert data
        jsonStr = json.dumps(capDict)
        
    except:
        print("Error")
        
    return jsonify(Capacity=jsonStr)

if __name__ == "__main__":
    # get config data
    data, network, A, B = parse_config()
    
    #listener listens from cryptoA
    # check to see if ark.db exists, if not initialize db, etc
    if os.path.exists('aces.db') == False:    
        acesdb = AceDB(A['dbusername'])
        # initalize sqldb object
        acesdb.setup()
    
    # check for new rewards accounts to initialize if any changed
    acesdb = AceDB(A['dbusername'])

    app.run(host = "192.168.1.116")