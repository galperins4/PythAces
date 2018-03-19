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

    def listen_transactions(self, ts):
        try:
            self.cursor.execute(f"""SELECT "id","senderId", "amount", "fee", "vendorField", "timestamp" FROM transactions WHERE "timestamp" > {ts} ORDER BY "rowId" DESC""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	    
	    
    def last_transaction(self):
        try:
            self.cursor.execute(f"""SELECT "timestamp" FROM transactions ORDER BY "rowId" DESC LIMIT 1""")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)	 