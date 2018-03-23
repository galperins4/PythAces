#!/usr/bin/env python
import requests

class Pythaces:
    def __init__(self, park, atomic):
        self.park = park
        self.atomic = atomic
        
    def service_capacity(self, address):
        cap = self.park.accounts().balance(address)
        self.capacity = int(cap['balance'])
        
        return self.capacity
    
    def reserve_capacity(self, contracts):
        s = 0
        for i in contracts:
            s+=i[5]
            
        self.reserve_capacity = s
        
        return self.reserve_capacity
    
    def available_capacity(self):
        self.available_capacity = self.capacity - self.reserve_capacity
        return self.available_capacity 
    
    def conversion_rate(self, a="ARK", b="KAPU"):
        url = "https://min-api.cryptocompare.com/data/pricemulti"
        fsyms = a+','+b
        tsyms = "USD"
        
        #set request params
        params = {"fsyms": fsyms,
                  "tsyms": tsyms}
        
        r = requests.get(url, params=params)
        
        self.conversion_rate = r.json[b][tsyms] / r.json[a][tsyms]
        
        return self.conversion_rate 