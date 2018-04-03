import psycopg2

class DB:
    def __init__(self, db, u, pw):
        self.connection = psycopg2.connect(
            dbname = db,
            user = u,
            password= pw,
            host='localhost',
            port='5432'
        )
        
        self.cursor=self.connection.cursor()

    def listen_transactions(self, row):
        try:
            self.cursor.execute(f"""SELECT "id","senderId", "recipientId", "amount", "fee", "vendorField", "timestamp" FROM transactions WHERE "rowId" > {row} ORDER BY "rowId" DESC""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	    
	    
    def last_transaction(self):
        try:
            self.cursor.execute(f"""SELECT "rowId" FROM transactions ORDER BY "rowId" DESC LIMIT 1""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	

    def listen_transactions_lisk(self,row):
        try:
            self.cursor.execute(f"""SELECT "id","senderId", "recipientId", "amount", "fee", "timestamp" FROM trs WHERE "rowId" > {row} ORDER BY "rowId" DESC""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	    
	    
    def last_transaction_lisk(self):
        try:
            self.cursor.execute(f"""SELECT "rowId" FROM trs ORDER BY "rowId" DESC LIMIT 1""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	
	
