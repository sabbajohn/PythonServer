import mysql.connector
class DB(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="objetiva",
        passwd="spqQVJ161",
        database="megasorte"
        )
        self.handler()
    
    def handler(self):
        return self.mydb