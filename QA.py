from DBConn import DBConn
from Ollama import Ollama

class QA:
    def __init__(self):
        self.dbconn = DBConn(path='/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db')
        self.ollama = Ollama()
    
    def query(self, question):
        prompt = "Tables in the DB along with their schema and a few examples:\n\n"
        names = self.dbconn.get_all_table_names()
        for name in names:
            prompt+='TABLE NAME: '+name+'\n'
            prompt+=self.dbconn.get_table_example(name)+'\n\n'
        prompt+='Narrow down the tables from the aforementioned list of tables can help answer the following question.'+'\n'
        prompt+='Question: '+question
        prompt+='\nGive your output in a json format as such:\n'
        prompt+='{"selected_tables":["name of first relevant table", "name of second relevant table",...,"name of last relevant table"}'
        prompt+='\nRemember that your output should only contain json and it should not contain any leading or trailing text, such that the output is directly parsable as a json'
        print(self.ollama.query(prompt)+'\n')


qa = QA()
while True:
    question = input('Input your question')
    if question=='end':
        break
    qa.query('Which country has the highest fuel consumption in 2024.')