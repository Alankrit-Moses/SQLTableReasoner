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
            prompt+=self.dbconn.get_table_example(name)+'\n\n'
        prompt+='Narrow down the tables from the aforementioned list of tables can help answer the following question.'+'\n'
        prompt+='Question: '+question+'\n\n'
        prompt+='Give your output in a json format as such:'
        prompt+='{"selected_tables":["name of first relevant table", "name of second relevant table",...,"name of last relevant table"}'
        prompt+='\nRemember that your output should only contain json and no leading or trailing text, so that I can directly parse the output as a json'
        print(prompt)
        # self.ollama.query(prompt)


qa = QA()
qa.query('')