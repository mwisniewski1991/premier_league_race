import streamlit as st
import pandas as pd
from data_manager.db.db_manager import DB_context_manager
import altair as alt

DB_PATH:str = 'data_manager/db/pl_race.sqlite'
SQL_SELECT:str = 'SELECT * FROM teams_race;'

with DB_context_manager(DB_PATH) as conn:
    df_plrace:pd.DataFrame = pd.read_sql(SQL_SELECT, conn)

st.set_page_config(page_title="Premier League Race", layout="wide")
st.title("Premier League Race")

domain:list[str] = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Burnley','Chelsea','Crystal Palace','Everton','Fulham','Liverpool','Luton Town','Manchester City','Manchester Utd','Newcastle Utd',"Nott'ham Forest",'Sheffield Utd','Tottenham','West Ham','Wolves']

range_:list[str] = ['#EF0107','#95bfe5','#c8102E','#CC0000','#0057B8','#6C1D45','#034694','#1B458F','#003399','#CC0000','#c8102E','orange','#6CABDD','#DA291C','#FFFFFF',"#DD0000",'#DA291C','#FFFFFF','#7A263A','#FDB913',]


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
                color=alt.Color(
                    'team_name', 
                    legend=alt.Legend(legendY=3, orient='bottom', direction='horizontal', titleAnchor='middle', title='Team name'),
                    scale=alt.Scale(domain=domain, range=range_)
                    )
                
                )
  
)

with st.container():
    st.altair_chart(pl_racechart, use_container_width=True)