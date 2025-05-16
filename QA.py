from DBConn import DBConn
from Ollama import Ollama
from constants import EXAMPLES

class QA:
    def __init__(self):
        self.dbconn = DBConn(path='/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db')
        self.ollama = Ollama()
        print(self.dbconn.get_table_example('marine_landings'))
    
    def sql_extractor(self, question, table_name, error_logs=''):
        prompt = '\n'.join(EXAMPLES)
        prompt+= '---END OF EXAMPLES---\n'
        prompt+= 'Actual table to be considered for SQL query:\n\nTable Name to be used in SQL query: '+table_name+'\n'
        prompt+= self.dbconn.get_table_example(table_name)
        prompt+='\nQuestion: '+question
        prompt+='\n\n'+error_logs
        prompt+='\n\nIMPORTANT: The output should only contain the SQL query, such that it can directly be executed.'
        answer = self.ollama.query(prompt)
        sql_query = answer.split('</think>')[1]
        return sql_query.strip()
    
    def sql_executor(self,question, table_name, max_tries=10):
        tries = 0
        sql_executed = 'select * from '+table_name
        final_result = ''
        errors = []
        while tries<max_tries:
            sql = self.sql_extractor(question,table_name,error_logs='\n\n'.join(errors) if errors!=[] else '')
            result = self.dbconn.query(sql)
            if result.contains('error'):
                errors.append('Query tried: '+sql+'\nError: '+result)
            else:
                final_result = result
                sql_executed = sql
                break
            tries+=1
        if final_result=='':
            result = self.dbconn.query(sql_executed)
        return [sql_executed, final_result]

        


qa = QA()
while True:
    question = input('Input your question: ')
    if question=='end':
        break
    print(qa.sql_executor(question,'marine_landings'))