from dash import Dash, html, dcc, Output, Input, ctx
# import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
from data_manager.db.db_manager import DB_context_manager
import pandas as pd

DB_PATH:str = 'app/data_manager/db/pl_race.sqlite'
SQL_SELECT:str = 'SELECT * FROM teams_race;'


with DB_context_manager(DB_PATH) as conn:
    df_plrace:pd.DataFrame = pd.read_sql(SQL_SELECT, conn)

app = Dash(__name__)

app.layout = html.Div(className='main', children=[
    html.Div(children=[
        html.H1('Premier League Race'),
        html.Div(dcc.Dropdown(sorted(df_plrace['team_name'].unique()), ['Arsenal', 'Manchester City'], id='plrace_dropdown', multi=True )),
        dcc.Graph(id='plrace_chart')
    ])
])

@app.callback(
    Output('plrace_chart', 'figure'),
    Input('plrace_dropdown', 'value')
)
def update_plrace_chart(teams_names):
    query:pd.Series = df_plrace['team_name'].isin(teams_names)
    fig:plotly.graph_objs.Figure = px.line(df_plrace[query], x='match_order', y='points_cum', color='team_name')

    fig.update_xaxes(visible=True , fixedrange=True, range=[1, 38])
    fig.update_yaxes(visible=True , fixedrange=True, range=[0, 100])


    fig.update_layout(
        xaxis_title="Points",
        yaxis_title="Match",
        margin=dict(t=10,l=10,b=10,r=10)
    )

    print(type(fig))
    return fig

if __name__ == '__main__':
    app.run(debug=True)