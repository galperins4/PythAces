#!/usr/bin/env python
import requests

class Conversion:
    def __init__(self, a="ARK", b="KAPU"):
        self.a = a
        self.b = b

    def conversion_rate(self):
        url = "https://min-api.cryptocompare.com/data/pricemulti"
        fsyms = self.a+','+self.b
        tsyms = "USD"
        
        #set request params
        params = {"fsyms": fsyms,
                  "tsyms": tsyms}
        
        r = requests.get(url, params=params)
        
        self.conversion_rate = r.json()[self.b][tsyms] / r.json()[self.a][tsyms]
        
        return self.conversion_rate 