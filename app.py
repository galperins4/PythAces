from flask import Flask, jsonify, request
from flask_cors import CORS
from core.acedb import AceDB
from core.pythaces import Pythaces
from core.contracts import Contract
from core.conversion import Conversion
from core.util import parse_config, get_network
import requests 
import time
import os.path

atomic = 100000000

app = Flask(__name__)
CORS(app)

@app.route("/api/<convCoin>", methods=['POST'])
def crypto(convCoin):
    acesdb = AceDB(coin['channel']['dbusername'])
    try:
        # get send/receive addresses and amouunt
        req_data = request.get_json()
        send = req_data['send']
        receive = req_data["receive"]
        amount = req_data["amount"]*atomic
        # do validations
        c1, c1_msg = validate_addresses(convCoin,send,receive)
        c2, c2_msg = validate_amount(convCoin,amount)

        a_check = all([c1, c2])

        if a_check == True:
    
            channel = coin['channel']['channel']
            # calculate value
            f = {'flatFee': coin['channel']['flat_fee'],
                 'pctFee': coin['channel']['pct_fee']} 

            c = Contract()
            send_amount, total_fee = c.pricing(channel,convCoin, amount, f)

            ts = int(time.time())
    
            c.create(ts, send, send_amount, receive, amount, total_fee, channel, convCoin)
            new_contract = (c.contract,)
            acesdb.storeContracts(new_contract)
            
            address = coin['channel']['service_acct'] 
            amt = send_amount / atomic
            vendorfield = c.uid
            
            qr_dict={"success":True,"channel":channel,"address":address,"amount":amt, "vendorField":vendorfield, "receive":(amount/atomic)} 
            #return json to client (address, amount, vendorfield)
            return jsonify(qr_dict)

        else:
            if c1:
                msg = c2_msg
            else:
                msg = c1_msg

        return jsonify(msg)
    
    except Exception as e:
        print(e)
        error ={"success":False, "msg":"Incorrect Entry"}
        return jsonify(Error=error)

#display all prices
@app.route("/api/prices")
def prices():
    
    try:
    	
        conversion_rates = {} 
        channel = coin['channel']['channel']
        # get conversion rates
        for key in coin:
            if key != "channel":
                cnv = Conversion(coin['channel']['channel'], key)
                conversion_rates[key] = cnv.conversion_rate()
                
        # get fees	
        feeDict = {
                "flatFee": coin['channel']['flat_fee'],
                "percentFee": coin['channel']['pct_fee']*100
                    }
        priceDict = {
                "channel": channel,
                "prices": conversion_rates,
                "fees": feeDict}
                
        return jsonify(priceDict)
    
    except Exception as e:
        print(e)
        error ={"success":False, "msg":"Prices not available"}
        return jsonify(Error=error)

def contract_to_json(c):
    convert={"contract":c[0],
         "createdOnTimestamp":c[1],
         "sendingAddress":c[2],
         "sendingAmount":c[3]/atomic,
         "receivingAddress":c[4],
         "receivingAmount":c[5]/atomic,
         "totalFees":c[6]/atomic,
         "contractStatus":c[7],
         "processedOnTimestamp":c[10],
         "channel": c[8],
         "coin": c[9],
         "serviceAccount": coin['channel']['service_acct']}
    
    return convert

#Change this to just send contracts
@app.route("/api/contracts") 
def contracts():
    acesdb = AceDB(coin['channel']['dbusername'])
    filtered_contracts=[]
    all_contracts = acesdb.contracts().fetchall()
    for i in all_contracts:
        if i[7] != "Expired":
            filter_tmp = contract_to_json(i)
            filtered_contracts.append(filter_tmp)

    return jsonify(filtered_contracts)

@app.route("/api/history/<id>")
def get_contract(id):
    acesdb = AceDB(coin['channel']['dbusername'])
    #contract_id = acesdb.singleContract(id).fetchall()
    all_contracts = acesdb.contracts().fetchall()
    for i in all_contracts:
        if i[0] == id:
            contract_id = i
   
    jsoned = contract_to_json(contract_id)
    return jsonify(jsoned)
    
#get all capacity
@app.route("/api/capacity")
def capacity():
    acesdb = AceDB(coin['channel']['dbusername'])
    try:
        service_availability = {}
        contracts = acesdb.unprocessedContracts().fetchall()
    
        for key in coin:
            if key != 'channel':
                pythaces = Pythaces(fx_coins[key], atomic)
                # total capacity
                capacity = pythaces.service_capacity(coin[key]['service_acct'])
                # reserve capacity
                reserved = pythaces.reserve_capacity(contracts, coin[key]['service_acct'])
                #available capacity
                available = pythaces.available_capacity()
        
                service_availability[key] = {"totalCapacity": capacity,
                                    "reservedCapacity": reserved,
                                    "availableCapacity": available}
        
        return jsonify(service_availability)
    
    except Exception as e:
        print(e)
        error ={"success":False, "msg":"Capacity is not available"}
        return jsonify(Error=error)

def validate_amount(c,amount):
    
    # check against limit 
    url = "http://"+coin['channel']['channel_ip']+"/api/capacity"
    r = requests.get(url)
    avail_cap = r.json()[c]["availableCapacity"] - atomic
    
    limit = 100*atomic
    if amount <= limit:
        if amount < avail_cap:
            flag = True
            m = amount
        else:
            flag = False
            m = "amount is currently over capacity"
    else:
        flag = False
        m = "amount is currently over capacity or limit" 

    
    msg = {"success":flag, "msg":m}
    return flag, msg


def validate_addresses(c, a_addr, b_addr):

    a_len=len(a_addr)
    b_len=len(b_addr)

    # set response to invalid
    flag = False
    msg = {"success":flag, "msg":"one or both addresses invalid, please double check"}
    
    # ark check
    if any([a_addr[0].isdigit(),b_addr[0].isdigit()]):
        # temp disable checks for non ark dpos coins
        
        flag = True
        msg = {"success": flag}
    else:
        # check that address is valid address length and network
        a_check = coin['channel']["service_acct"][0]
        b_check = coin[c]["addr_start"]
        
        all_check= all([a_len==34,a_addr[0]==a_check,b_len==34,b_addr[0]==b_check])
        if all_check:
        # both addresses are good, flip flag and message
            flag = True
            msg = {"success": flag}

    return flag, msg

if __name__ == "__main__":
    # get config data
    network, coin = parse_config()
    
    #initialize park objects for use
    fx_coins = {}
    for key in coin:
        if key != "channel":
            fx_coins[key] = get_network(key, network, coin[key]['relay_ip'])
    app.run(threaded=True)
