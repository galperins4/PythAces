from uuid import uuid4

class Contract:
    def __init__(self):
        self.contract = ()
        self.uid = str(uuid4())
        self.contract = self.contract + (self.uid,)
        
    def create(self, ts, saddr, samt, raddr, ramt, fee):
        self.contract = self.contract + (ts, saddr, samt, raddr, ramt, fee)
        return (self.contract,)
