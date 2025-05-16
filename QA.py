from DBConn import DBConn
from Ollama import Ollama
from constants import EXAMPLES

class QA:
    def __init__(self):
        self.dbconn = DBConn(path='/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db')
        self.ollama = Ollama()
        print(self.dbconn.get_table_example('marine_landings'))
    
    def sql_extractor(self, question, table_name):
        prompt = '\n'.join(EXAMPLES)
        prompt+= '---END OF EXAMPLES---\n'
        prompt+= 'Actual table to be considered for SQL query:\n\nTable Name to be used in SQL query: '+table_name+'\n'
        prompt+= self.dbconn.get_table_example(table_name)
        prompt+='\nQuestion: '+question
        prompt+='\n\nIMPORTANT: The output should only contain the SQL query, such that it can directly be executed. Do not produce the think tokens or the <think> block.'
        answer = self.ollama.query(prompt)


qa = QA()
while True:
    question = input('Input your question: ')
    if question=='end':
        break
    qa.query(question,'marine_landings')