from DBConn import DBConn
from Ollama import Ollama

class QA:
    def __init__(self):
        self.dbconn = DBConn(path='/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db')
        self.ollama = Ollama()
    
    def query(self, question, table_name):
        examples = [
            "Generate SQL given the question and table for selecting the required rows and columns to answer the question correctly.\nFollowing are some examples:",
            "",
            "Table_title: Marek Plawgo",
            "Table_columns: ['Year', 'Competition', 'Venue', 'Position', 'Event', 'Notes']",
            "Question: when was his first 1st place record?",
            "output: Let's think step by step.",
            "columns: ['Year',  'Position']",
            "sql: select Year, Position from T where Position like '%1st%'",
            "",
            "Table_title: 2013\u201314 Toros Mexico season",
            "Table_columns: ['Game', 'Day', 'Date', 'Kickoff', 'Opponent', 'Results_Score', 'Results_Record', 'Location', 'Attendance']",
            "Question: what was the number of people attending the toros mexico vs. monterrey flash game?",
            "output: Let's think step by step.",
            "columns: ['Attendance’, 'Opponent']",
            "sql: select Opponent, Attendance from T where Opponent like '%monterrey flash%'",
            "",
            "Table_title: Radhika Pandit",
            "Table_columns:  ['Year', 'Film', 'Role', 'Language', 'Notes']",
            "Question: what is the total number of films with the language of kannada listed?",
            "output: Let's think step by step.",
            "columns: ['Film', 'Language']",
            "sql: select Film, Language from T where Language like '%kannada%'",
            "",
            "Table_title: List of storms on the Great Lakes",
            "Table_columns:  ['Ship', 'Type_of_Vessel', 'Lake', 'Location', 'Lives_lost']",
            "Question: how many more ships were wrecked in lake huron than in erie?",
            "output: Let's think step by step.",
            "columns: ['Ship',  'Lake']",
            "sql: SELECT Ship, Lake FROM T WHERE Lake LIKE '%Lake Huron%' or Lake LIKE '%Lake Erie%'",
            "",
            "Table_title: List of hospitals in North Carolina",
            "Table_columns:  ['Name', 'City', 'Hospital_beds', 'Operating_rooms', 'Total', 'Trauma_designation', 'Affiliation', 'Notes']",
            "Question: what is the only hospital to have 6 hospital beds?",
            "output: Let's think step by step.",
            "columns: ['Name', 'Hospital_beds']  ",
            "sql: select Name, Hospital_beds from T where Hospital_beds = 6",
            "",
            "Table_title:Churnet Valley Railway ",
            "Table_columns:  ['Number', 'Name', 'Type', 'Livery', 'Status', 'Notes']",
            "Question: how many locomotives are currently operational?",
            "output: Let's think step by step.",
            "columns: ['Name',  'Status']",
            "sql: select Name, Status from T where Status like '%operational%'",
            "",
            "Table_title: List of hospitals in North Carolina",
            "Table_columns:  ['Rank', 'Nation', 'Gold', 'Silver', 'Bronze', 'Total']",
            "Question: who won the most gold medals?",
            "output: Let's think step by step.",
            "columns: ['Nation', 'Gold'] ",
            "sql: select Nation, Gold from T",
            "",
            "Table_title: 2012–13 Exeter City F.C. season",
            "Table_columns:  ['Name', 'League', 'FA_Cup', 'League_Cup', 'JP_Trophy', 'Total']",
            "Question: does pat or john have the highest total?",
            "output: Let's think step by step.",
            "columns: ['Name', 'Total']",
            "sql: select Name, Total from T where Name like '%pat%' or Name like '%john%'",
            "",
            "Table_title: My Brother and Me",
            "Table_columns:  ['Series_', 'Season_', 'Title', 'Notes', 'Original_air_date']",
            "Question: alfie's birthday party aired on january 19. what was the airdate of the next episode?",
            "output: Let's think step by step.",
            "columns: ['Title', 'Season_', 'Original_air_date']",
            "sql: select Title, Season_, Original_air_date from T",
            "",
            "Table_title: The Harvest (Boondox album)  ",
            "Table_columns:  ['_', 'Title', 'Time', 'Lyrics', 'Music', 'Producers', 'Performers']",
            "Question: how many song come after \"rollin hard\"?",
            "output: Let's think step by step.",
            "columns: ['Title', 'Time']",
            "sql: select Title, Time from T",
            "",
            "Table_title: GameStorm.org",
            "Table_columns:  ['Iteration', 'Dates', 'Location', 'Attendance', 'Notes']",
            "Question: what's the total attendance for gamestorm 11?",
            "output: Let's think step by step.",
            "columns: ['Attendance', 'Iteration']",
            "sql: select Attendance, Iteration from T where Iteration like '%gamestorm 11%'",
            "",
            "Table_title: 1981 Iowa Hawkeyes football team ",
            "Table_columns:  ['Date', 'Opponent', 'Rank', 'Site', 'TV', 'Result', 'Attendance']",
            "Question: which date had the most attendance?",
            "output: Let's think step by step.",
            "columns: ['Date', 'Attendance']",
            "sql: select Date, Attendance from T",
            "\n"]
        
        prompt = '\n'.join(examples)
        prompt+= '---END OF EXAMPLES---\n'
        prompt+= 'Actual table to be considered for SQL query:\n\nTable Name to be used in SQL query: '+table_name+'\n'
        prompt+= self.dbconn.get_table_example(table_name)
        prompt+='\nQuestion: '+question
        prompt+='\n\nIMPORTANT: The output should only contain the SQL query, such that it can directly be executed.'
        print(self.ollama.query(prompt))


qa = QA()
while True:
    question = input('Input your question: ')
    if question=='end':
        break
    qa.query(question)