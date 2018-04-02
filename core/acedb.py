import sqlite3
import time
import threading

lock = threading.Lock()

class AceDB:
    def __init__(self, u):
        self.connection=sqlite3.connect('/home/'+u+'/PythAces/aces.db', check_same_thread=False)
        self.cursor=self.connection.cursor()

    def commit(self):
        return self.connection.commit()

    def execute(self, query, args=[]):
        try:
            lock.acquire(True)
            res = self.cursor.execute(query, args)
        finally:
            lock.release()
            
        return res

    def executemany(self, query, args):
        try:
            lock.acquire(True)
            res = self.cursor.executemany(query, args)
        finally:
            lock.release()
        
        return res

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contracts (contract varchar(64), timestamp int, s_addr varchar(36), s_amt bigint, r_addr varchar(36), r_amt bigint, c_fee bigint, status varchar(36), processed_at varchar(64) null)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (contract varchar(64), address varchar(36), amount varchar(64), id varchar(64), processed_at varchar(64) )")
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS staging (contract varchar(64), address varchar(36), payamt bigint, msg varchar(64), processed_at varchar(64) null )")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS rows (row bigint) ")
        
        self.connection.commit()

    def storeRow(self,row):
        r=[]
        r.append((row))
        self.execute("INSERT INTO rows VALUES (?)", r)
        self.commit()

    def updateRow(self,row):
        start = 1        
        self.cursor.execute(f"UPDATE rows SET row = {row} WHERE rowid = {start}")
        self.commit()
        
    def getRows(self):
        return self.cursor.execute("SELECT * FROM rows")
     
    def storeContracts(self, contracts):
        newContracts=[]
        
        for c in contracts:
            self.cursor.execute("SELECT contract FROM contracts WHERE contract = ?", (c[0],))

            if self.cursor.fetchone() is None:
                newContracts.append((c[0], c[1], c[2], c[3], c[4], c[5], c[6],"Pending Confirmation", None))

        self.executemany("INSERT INTO contracts VALUES (?,?,?,?,?,?,?,?,?)", newContracts)

        self.commit()
    
    def storePayment(self, contract, address, amount, msg):
        staging=[]

        staging.append((contract, address, amount, msg, None))

        self.executemany("INSERT INTO staging VALUES (?,?,?,?,?)", staging)

        self.commit()
        
    def storeTransactions(self, tx):
        newTransactions=[]
        
        ts = int(time.time())
        
        for t in tx:
            self.cursor.execute("SELECT id FROM transactions WHERE id = ?", (t[3],))
            
            if self.cursor.fetchone() is None:
                newTransactions.append((t[0], t[1], t[2], t[3], ts))
                
        self.executemany("INSERT INTO transactions VALUES (?,?,?,?,?)", newTransactions)
        
        self.commit()
        
    def markAsProcessed(self, contract):
        ts = int(time.time())
        msg = "Processed"
        self.cursor.execute(f"UPDATE contracts SET status = '{msg}', processed_at = '{ts}' WHERE contract = '{contract}'")
        self.commit()
        
    def expireContract(self, contract):
        ts = int(time.time())
        expired = "Expired"
        self.cursor.execute(f"UPDATE contracts SET status = '{expired}', processed_at = '{ts}' WHERE contract = '{contract}'")
        self.commit()
        
    def contracts(self):
        return self.cursor.execute("SELECT * FROM contracts")
    
    def singleContract(self, id):
        return self.cursor.execute("SELECT * FROM contracts WHERE contract = '{id}'")
    
    def transactions(self):
        return self.cursor.execute("SELECT * FROM transactions")
    
    def stagedArkPayment(self):
        return self.cursor.execute("SELECT rowid, * FROM staging WHERE processed_at IS NULL LIMIT 40")

    def processedContracts(self):
        return self.cursor.execute("SELECT * FROM contracts WHERE processed_at NOT NULL")

    def unprocessedContracts(self):
        return self.cursor.execute("SELECT * FROM contracts WHERE processed_at IS NULL")
  
    def processStagedPayment(self, contract):
        ts = int(time.time())
        
        self.cursor.execute(f"UPDATE staging SET processed_at = '{ts}' WHERE contract = '{contract}'")
        self.commit()

