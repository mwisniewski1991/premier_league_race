import sqlite3

DB_PATH = 'pl_race.sqlite'

class DB_context_manager:
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        
    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path) 
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.conn.close()

def create_table(conn:sqlite3.Connection) -> None:
    sql_create:str = '''
        CREATE TABLE IF NOT EXISTS teams_race
        (
            team_name TEXT, 
            match_order INTEGER, 
            points INTEGER,
            points_cum INTEGER
        )
    '''
    conn.execute(sql_create)

def insert_data(conn:sqlite3.Connection, data:list[tuple]) -> None:
    sql_insert:str = 'INSERT INTO teams_race VALUES(?,?,?,?);'
    conn.executemany(sql_insert, data)
    conn.commit()

def delete_all_rows(conn:sqlite3.Connection) -> None:
    sql_delete = 'DELETE FROM teams_race;'
    conn.execute(sql_delete)
    conn.commit()    

def get_all_data(conn:sqlite3.Connection) -> None:
    sql_select = 'SELECT * FROM teams_race;'
    cursor:sqlite3.Cursor = conn.cursor()

    result:list[tuple] = cursor.fetchmany(sql_select)
    return result

def main() -> None:
    with DB_context_manager(DB_PATH) as conn:
        get_all_data(conn)
    

if __name__ == '__main__':
    main()