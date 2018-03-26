#!/usr/bin/env python
class Pythaces:
    def __init__(self, park, atomic):
        self.park = park
        self.atomic = atomic
        
    def service_capacity(self, address):
        cap = self.park.accounts().balance(address)
        self.capacity = int(cap['balance'])
        
        return self.capacity
    
    def reserve_capacity(self, contracts, letter):
        s = 0
        # loop through contracts
        for i in contracts:
            # check for starting letter of send to address for network
            if i[4][0] == letter:
                s+=i[5]
            
        self.reserve_capacity = s
        
        return self.reserve_capacity
    
    def available_capacity(self):
        self.available_capacity = self.capacity - self.reserve_capacity
        return self.available_capacity 