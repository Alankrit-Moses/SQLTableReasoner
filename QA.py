from DBConn import DBConn
from Ollama import Ollama

class QA:
    def __init__(self):
        self.dbconn = DBConn()
        self.ollama = Ollama()
    
    def query(self, question):
        prompt = "Tables in the DB:\n"
        print(prompt,self.dbconn.get_all_table_names())