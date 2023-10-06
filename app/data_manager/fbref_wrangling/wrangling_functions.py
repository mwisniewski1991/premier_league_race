import pandas as pd

def get_table(link:str) -> pd.DataFrame:
    html_data:list[pd.DataFrame] = pd.read_html(link)
    return html_data[0]

def dropna(df:pd.DataFrame, drop_based_on:str) -> pd.DataFrame:
    return df.dropna(subset=drop_based_on).copy()

def drop_columns(df:pd.DataFrame, columns_to_drop:list[str]) -> pd.DataFrame:
    return df.drop(columns=columns_to_drop)


def extract_teams_score(df:pd.DataFrame, score_column:str) -> pd.DataFrame:
    df[['home_score', 'away_score']] = df[score_column].str.split(pat='–',expand=True).astype('float16')
    return df

def calculate_teams_points(home_score:float, away_score:float, calc_for_team:str='home') -> pd.DataFrame:
    if calc_for_team == 'home':
        if home_score > away_score:
            return 3
        if home_score == away_score:
            return 1
        return 0 
    if calc_for_team == 'away':
        if home_score < away_score:
            return 3
        if home_score == away_score:
            return 1
        return 0 

def extract_teams_points(df:pd.DataFrame, home_score_column:str, away_score_columns:str, calc_for_team:str='home') -> pd.DataFrame:
    temp_series =  df[[home_score_column, away_score_columns]].apply(lambda row: calculate_teams_points(row[home_score_column], row[away_score_columns], calc_for_team), axis=1)
    df[f'{calc_for_team}_points'] = pd.DataFrame(temp_series)
    return df


def create_datatime(df:pd.DataFrame, date_column:str, time_column:str):
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    return df


def create_race_table(df:pd.DataFrame) -> pd.DataFrame:
    teams_set:set[str] = {*df['Home'].unique().tolist(), *df['Away'].unique().tolist(),}
    new_tables_list:list[pd.DataFrame] = []
    
    for team in teams_set:

        team_table:pd.DataFrame =  df.query(f' Home == "{team}" or Away == "{team}" ').copy()
        match_order:pd.Series = team_table['datetime'].rank()
        points:pd.Series = team_table.apply(lambda row: row['home_points'] if row['Home'] == team else row['away_points'], axis=1)
        points_cum:pd.Series = points.cumsum()

        new_tables_list.append(
            pd.DataFrame({
            'team_nam': team,
            'match_order':match_order,
            'points': points,
            'points_cum': points_cum,
            }))
        
    return pd.concat(new_tables_list)
