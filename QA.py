from DBConn import DBConn
from Ollama import Ollama
from constants import SQL_EXAMPLES, ANSWER_EXAMPLES

class QA:
    def __init__(self,think=True):
        self.dbconn = DBConn(path='/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db')
        self.ollama = Ollama()
        self.think = think
    
    def sql_extractor(self, question, table_name, error_logs=''):
        prompt = '\n'.join(SQL_EXAMPLES)
        prompt+= '---END OF EXAMPLES---\n'
        prompt+= 'Actual table to be considered for SQL query:\n\nTable Name to be used in SQL query: '+table_name+'\n'
        prompt+= self.dbconn.get_table_info(table_name)
        prompt+= '\n\nA few rows from the table to portray the value types:\n'
        prompt+= self.dbconn.get_table_example(table_name)
        prompt+='\n\nQuestion: '+question
        prompt+='\n\n'+error_logs
        prompt+='\n\nIMPORTANT: The output should only contain the SQL query, such that it can directly be executed.'
        if not self.think:
            prompt+='\n/no_think'
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
            result = self.dbconn.run(sql)
            if 'error' in result:
                errors.append('Query tried: '+sql+'\nError: '+result)
            else:
                final_result = result
                sql_executed = sql
                break
            tries+=1
        if final_result=='':
            result = self.dbconn.run(sql_executed)
        return [sql_executed, final_result]
    
    def generate_answer(self, question, table_name):
        prompt = '\n'.join(ANSWER_EXAMPLES)
        prompt+= "Table name: "+table_name
        prompt+= "\n"+self.dbconn.get_table_info(table_name)
        sql_results = self.sql_executor(question, table_name)
        prompt+= '\n\nSQL QUERY: '+sql_results[0]+'\nRESULTS:\n'+sql_results[1]
        prompt+='\n\n Based on the result of the query executed on the aforementioned table, give the answer to the question.'
        prompt+='\nQuestion: '+question
        if not self.think:
            prompt+='\n/no_think'
        #Printing info before final answer
        print(table_name)
        print(self.dbconn.get_table_info(table_name))
        print('\nSQL QUERY: '+sql_results[0]+'\nRESULTS:\n'+sql_results[1])
        return self.ollama.query(prompt).split('</think>')[1].strip()

# think=True for reasoning
qa = QA(think=False)
while True:
    question = 'Did Peru have the highest value in 1997?'
    # question = input('Input your question: ')
    # if question=='end':
    #     break
    print(qa.generate_answer(question,'marine_landings'))
    break