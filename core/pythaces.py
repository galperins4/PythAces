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
                # look for non ark account
                if addr[0].isdigit():
                     a1 = addr.translate({ord(ch): None for ch in '0123456789'}).lower()
                     
a2 = addr.translate({ord(ch): None for ch in '0123456789'}).lower()
                else:    
                    if i[4][0] == addr[0]:
                        s+=i[5]
            
        self.reserve_capacity = s
        
        return self.reserve_capacity
    
    def available_capacity(self):
        self.available_capacity = self.capacity - self.reserve_capacity
        return self.available_capacity 
