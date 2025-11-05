from zapros import *
import sqlite3
from contextlib import contextmanager

class DB:
    def __init__(self,db_name = 'victorina.db'):
        self.db_name = db_name

    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для управления соединением."""
        conn = sqlite3.connect(self.db_name)
        # тип а-ля словарь
        #conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def create_table(self, query=CREATE_VICTOR):
        # запрещаем делать SQL-инъекции
        query = query.replace('--', '')
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(PRAGMA)
            cursor.execute(query)
            conn.commit()
            return cursor.fetchall()

    def create_lines(self, table_name, columns, data) -> int:
        """Создание новой записи."""
        table_name = table_name.replace('--', '')
        columns = columns.replace('--', '')
        s = '?, ' * len(columns.split(','))
        # "INSERT INTO questions (txt, right, wrong, score) VALUES (?, ?, ?, ?)", ('Кто?', "Я", "Ты,Он,Мы", 1)
        # "INSERT INTO questions (txt, right, wrong, score) VALUES ('Кто?', "Я", "Ты,Он,Мы", 1)"
        if type(data) == str:
            data = [data]
        query = f"INSERT INTO {table_name} {columns} VALUES ({s[:-2]})"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return cursor.lastrowid
        
    def execute(self,zapros,data=[]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(zapros,data)
            conn.commit()
            return cursor.fetchall()
        
if __name__ == "__main__":
    db = DB()
    db.execute(DROP+'victorina')
    db.execute(DROP+'questions')
    db.execute(DROP+'content')
    db.create_table(CREATE_VICTOR)
    db.create_table(CREATE_Q)
    db.create_table(CREATE_CON)
    for vic in VS:
        last_id = db.create_lines('victorina','(name)',vic)
    print(last_id)
    for q in QS:
        last_id = db.create_lines('questions','(txt,right_ans,wrong,score)',q)
    print(last_id)
    for con in CONTENT:
        last_id = db.create_lines('content','(v_id,q_id)',con)
    print(last_id)
    print( db.execute(SELECT+'questions'))

