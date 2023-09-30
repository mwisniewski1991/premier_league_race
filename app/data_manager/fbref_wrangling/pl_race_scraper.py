import pandas as pd
from fbref_wrangling import wrangling_functions

def scrap_plrace_data() -> list[tuple]:

    FBREF_LINK:str = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    
    pl_table = wrangling_functions.get_table(FBREF_LINK)
    pl_table = (
    pl_table
        .pipe(wrangling_functions.dropna, 'Score')
        .pipe(wrangling_functions.extract_teams_score, 'Score')
        .pipe(wrangling_functions.extract_teams_points, 'home_score', 'away_score', 'home')
        .pipe(wrangling_functions.extract_teams_points, 'home_score', 'away_score', 'away')
        .pipe(wrangling_functions.create_datatime, 'Date', 'Time')
        .pipe(wrangling_functions.drop_columns, ['Wk', 'Day', 'Venue', 'Referee', 'Match Report', 'Notes', 'Date', 'Time'])
        .pipe(wrangling_functions.create_race_table)
    )

    return pl_table.to_records(index=False).tolist()



if __name__ == '__main__':
    scrap_plrace_data()