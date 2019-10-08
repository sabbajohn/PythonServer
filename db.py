import mysql.connector
class db(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="objetiva",
        passwd="spqQVJ161",
        database="megasorte"
        )
        self.haldler()
    
    def handler(self):
        return self.mydb