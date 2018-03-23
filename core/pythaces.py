#!/usr/bin/env python


class Pythaces:
    def __init__(self, park):
        self.park = park
        
    def service_capacity(self, address):
        cap = self.park.accounts().balance(address)
        self.capacity = cap['balance']
        
        return self.capacity
    
    def reserve_capacity(self, contracts):
        s = 0
        for i in contracts:
            s+=i[5]
            
        self.reserve_capacity = s
        
        return self.reserve_capacity
    
    def available_capacity(self):
        return self.capacity - self.reserve_capacity
    
    def conversion_rate(self):
        pass