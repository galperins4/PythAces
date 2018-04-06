#!/usr/bin/env python
class Pythaces:
    def __init__(self, park, atomic):
        self.park = park
        self.atomic = atomic
        
    def service_capacity(self, address):
        try:
            cap = self.park.accounts().balance(address)
            self.capacity = int(cap['balance'])
        except Exception as e:
            print(e)
            self.capacity = 0
        
        return self.capacity
    
    def reserve_capacity(self, contracts, addr):
        s = 0
        # loop through contracts
        if contracts:
            for i in contracts:
                # check for starting letter of send to address for network
                if i[4][0] == letter:
                    s+=i[5]
            
        self.reserve_capacity = s
        
        return self.reserve_capacity
    
    def available_capacity(self):
        self.available_capacity = self.capacity - self.reserve_capacity
        return self.available_capacity 
