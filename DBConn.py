import sqlite3
from pathlib import Path

class DBConn:
    def __init__(self, path):
        self.db_path = Path(path)

    def get_all_table_names(self):
        names = self.run("SELECT name AS table_names FROM sqlite_master WHERE type='table'",postprocess=False)
        return names[0]
    
    def get_table_example(self, table_name, top_k=3):
        return self.run("SELECT * FROM "+table_name+" LIMIT "+str(top_k))

    def _rows_to_str(self, cursor, rows):
        if not rows:
            return "(no rows)"
        cols = [d[0] for d in cursor.description]
        widths = [
            max(len(str(row[c])) for row in rows + [dict(zip(cols, cols))])
            for c in cols
        ]
        header = " | ".join(n.ljust(w) for n, w in zip(cols, widths))
        body = "\n".join(
            " | ".join(str(r[c]).ljust(w) for c, w in zip(cols, widths))
            for r in rows
        )
        return f"{header}\n{'-' * len(header)}\n{body}"

    def run(self, sql, postprocess=True):
        sql = sql.strip().rstrip(";") + ";"
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute(sql)
                if not postprocess:
                    return cur.fetchall()    
                return self._rows_to_str(cur, cur.fetchall())
        except sqlite3.Error as e:
            return f"SQLite error: {e}"

# db = DBConn("/projects/oecd/oecd-prod-test/oecd-factchecks/OECD_Data.db")
# print(db.get_all_table_names())