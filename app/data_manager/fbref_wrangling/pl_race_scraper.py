from fbref_wrangling import pl_race_wrangling_functions

def scrap_plrace_data() -> list[tuple]:

    FBREF_LINK:str = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    
    pl_table = pl_race_wrangling_functions.get_table(FBREF_LINK)
    pl_table = (
    pl_table
        .pipe(pl_race_wrangling_functions.dropna, 'Score')
        .pipe(pl_race_wrangling_functions.extract_teams_score, 'Score')
        .pipe(pl_race_wrangling_functions.extract_teams_points, 'home_score', 'away_score', 'home')
        .pipe(pl_race_wrangling_functions.extract_teams_points, 'home_score', 'away_score', 'away')
        .pipe(pl_race_wrangling_functions.create_datatime, 'Date', 'Time')
        .pipe(pl_race_wrangling_functions.drop_columns, ['Wk', 'Day', 'Venue', 'Referee', 'Match Report', 'Notes', 'Date', 'Time'])
        .pipe(pl_race_wrangling_functions.create_race_table)
    )

    return pl_table.to_records(index=False).tolist()



if __name__ == '__main__':
    scrap_plrace_data()