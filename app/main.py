import streamlit as st
import pandas as pd
from data_manager.db.db_manager import DB_context_manager
import altair as alt

DB_PATH:str = 'app/data_manager/db/pl_race.sqlite'
SQL_SELECT:str = 'SELECT * FROM teams_race;'

with DB_context_manager(DB_PATH) as conn:
    df_plrace:pd.DataFrame = pd.read_sql(SQL_SELECT, conn)

st.set_page_config(page_title="Premier League Race", layout="wide")
st.title("Premier League Race")


with st.sidebar:
    teams_names = st.multiselect('Choose Clubs', sorted(df_plrace['team_name'].unique()), ['Arsenal', 'Manchester City'])

    # for team in sorted(df_plrace['team_name'].unique()):
    #     print(team)
    #     st.checkbox(team, value=team)
    

    
pl_racechart = (
    alt.Chart(df_plrace[df_plrace['team_name'].isin(teams_names)])
        .mark_line()
        .encode(
                x = alt.Y('match_order', title='Match', scale=alt.Scale(domain=[1,36])),
                y = alt.Y('points_cum', title='Points', scale=alt.Scale(domain=[0,100])),
                color='team_name')
  
)

with st.container():
    st.altair_chart(pl_racechart, use_container_width=True)