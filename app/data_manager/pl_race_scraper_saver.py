from fbref_wrangling import pl_race_scraper
from db import db_manager 
from db.db_manager import DB_context_manager

DB_PATH = 'data_manager/db/pl_race.sqlite'

def main() -> None:
    plrace_data:list[tuple] = pl_race_scraper.scrap_plrace_data()

    with DB_context_manager(DB_PATH) as conn:
        db_manager.create_table(conn)
        db_manager.delete_all_rows(conn)
        db_manager.insert_data(conn, plrace_data)

if __name__ == '__main__':
    main()