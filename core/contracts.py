#!/usr/bin/env python

from uuid import uuid4
from .conversion import Conversion
atomic = 100000000


class Contract:
    def __init__(self):
        self.contract = ()
        tmp = str(uuid4())
        self.uid = unicode(tmp, "utf-8")
        self.contract = self.contract + (self.uid,)
        
    def create(self, ts, saddr, samt, raddr, ramt, fee):
        self.contract = self.contract + (ts, saddr, samt, raddr, ramt, fee)
        return self.contract
       
    def pricing(self,a,b,amt,fees):
        cnv = Conversion(a, b)
        
        rate= cnv.conversion_rate()
        convert_amount = amt*rate
        
        f_fee = fees['flat_fee']*atomic
        p_fee = fees['pct_fee']*convert_amount
        total_fee = int((p_fee + f_fee))
        send_amount = int((convert_amount)) + total_fee
        
        return send_amount, total_fee
    	
