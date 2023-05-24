# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import visdcc
# Incorporate data
mychess_games_df = pd.read_csv('preprocessed_data.csv')
mychess_games_df = mychess_games_df.sort_values(by='end_time', ascending=False)
mychess_games_df = mychess_games_df.rename(columns={'oppenings':'openings'}).reset_index()
mychess_games_df['openings']= mychess_games_df['openings'].replace('-', ' ', regex=True)
mychess_games_stats_df=  mychess_games_df.groupby(['time_class','result']).agg(total=('result',np.size)).reset_index()
print(mychess_games_stats_df)
blitz_result = mychess_games_stats_df[mychess_games_stats_df['time_class']=='blitz']['result'].to_list()
blitz_total = mychess_games_stats_df[mychess_games_stats_df['time_class']=='blitz']['total'].to_list()
bullet_result = mychess_games_stats_df[mychess_games_stats_df['time_class']=='bullet']['result'].to_list()
bullet_total = mychess_games_stats_df[mychess_games_stats_df['time_class']=='bullet']['total'].to_list()
rapid_result = mychess_games_stats_df[mychess_games_stats_df['time_class']=='rapid']['result'].to_list()
rapid_total = mychess_games_stats_df[mychess_games_stats_df['time_class']=='rapid']['total'].to_list()
oppening_df = mychess_games_df.groupby('openings').agg(game_count = ('black.rating',np.size)).reset_index()
top_open = oppening_df.sort_values(by = 'game_count',ascending=False).reset_index(drop=True).head(10)
white_openings= mychess_games_df[mychess_games_df.my_colour=='white'].groupby(['openings','result']).agg(game_count = ('white.rating',np.size)).reset_index()
top_white_wins=white_openings[white_openings.result=='win'].sort_values(by = 'game_count',ascending=False).head(3)
top_white_losses= white_openings[white_openings.result=='lose'].sort_values(by = 'game_count',ascending=False).head(3)
black_openings= mychess_games_df[mychess_games_df.my_colour=='black'].groupby(['openings','result']).agg(game_count = ('white.rating',np.size)).reset_index()
top_black_wins= black_openings[black_openings.result=='win'].sort_values(by = 'game_count',ascending=False).head(3)
top_black_losses= black_openings[black_openings.result=='lose'].sort_values(by = 'game_count',ascending=False).head(3)
plot_list=['all', 'rapid-timeseries', 'blitz-timeseries','bullet-timeseries','world-map'
           ,'white-cap-dist','black-cap-dist','time-per-move','game-stats']

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    visdcc.Run_js(id='javascript'), dbc.Container([ 
    dbc.Row([
        html.Div('Chess.com Dashboard', className="text-primary text-center fs-3")
    ]),
    
    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in plot_list],
                    value='all',
                    inline=True,
                    id='radio-buttons-final')
    ]),
        
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data = mychess_games_df[['white.username','black.username','result','time_class','my_rating','end_time']].to_dict('records'), 
            page_size=5, style_table={'overflowX': 'auto'},
            style_as_list_view=True,
            style_cell={'whiteSpace': 'normal',
                        'height': 'auto',
                        'padding': '5px',
                        'backgroundColor':  'lavender'},
            style_header={
                        'backgroundColor': 'paleturquoise',
                        'fontWeight': 'bold'},)
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
        html.Div('Top Openings', className=" text-center fs-3")
    ]),
            dash_table.DataTable(
    data=top_open.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in top_open.columns],
    style_as_list_view=True,
    style_cell={'whiteSpace': 'normal',
                'height': 'auto',
                'padding': '5px',
               'backgroundColor':  'lavender'},
    style_header={
        'backgroundColor': 'paleturquoise',
        'fontWeight': 'bold'
    },
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Openings']
    ],
)
            # dcc.Graph(figure=go.Figure(data=[go.Table(
            #                 header=dict(values=list(top_open.columns),
            #                             fill_color='paleturquoise',
            #                             align='left'
            #                             ),
            #                 cells=dict(values=[top_open.openings, top_open.game_count],
            #                         fill_color='lavender',
            #                         align='left'))]))
                    
              ], width=5),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                            html.Div('White Wins', className=" text-center")
                            ]),
                    dash_table.DataTable(data=top_white_wins[['openings','game_count']].to_dict('records'), page_size=12, style_table={'overflowX': 'auto'},
                    style_cell={'whiteSpace': 'normal',
                'height': 'auto'})
                ],width=6),
                dbc.Col([dbc.Row([
                            html.Div('White Losses', className=" text-center")
                            ]),
    
                    dash_table.DataTable(data=top_white_losses[['openings','game_count']].to_dict('records'), page_size=12, style_table={'overflowX': 'auto'},
                    style_cell={'whiteSpace': 'normal',
                'height': 'auto'})
                ],width=6),
        ]),
            dbc.Row([
                dbc.Col([dbc.Row([
                            html.Div('Black Wins', className=" text-center")
                            ]),dash_table.DataTable(data=top_black_wins[['openings','game_count']].to_dict('records'), page_size=12, style_table={'overflowX': 'auto'},
                    style_cell={'whiteSpace': 'normal',
                'height': 'auto'})
                ],width=6),
                dbc.Col([dbc.Row([
                            html.Div('Black Losses', className=" text-center ")
                            ]),dash_table.DataTable(data=top_black_losses[['openings','game_count']].to_dict('records'), page_size=12, style_table={'overflowX': 'auto'},
                    style_cell={'whiteSpace': 'normal',
                'height': 'auto'})
                ],width=6),
        ]),
        ], width=7),
    ]),
html.Hr()
], fluid=True),
])

@app.callback(
    Output('javascript', 'run'),
    [Input(component_id='radio-buttons-final', component_property='value')])

def resize(_): 
    return "console.log('resize'); window.dispatchEvent(new Event('resize'));"

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
    # ,Input(component_id='radio-buttons-1', component_property='value')
)
def update_graph(col_chosen):
    if col_chosen=='bullet-timeseries':
        blitz = mychess_games_df[mychess_games_df['time_class']=='bullet'][['end_time','my_rating','result']]
        fig = px.line(x=blitz.groupby("end_time")["my_rating"].mean().keys(), y=blitz.groupby("end_time")["my_rating"].mean().values, markers=True,line_shape='hv',color=blitz['result'])
        fig.update_layout(title_text="bullet rating timeseries based on result", xaxis={'title':'date and time'}, yaxis={'title':'bullet rating'})
        return fig
        
    elif col_chosen=='rapid-timeseries': 
        blitz = mychess_games_df[mychess_games_df['time_class']=='rapid'][['end_time','my_rating','result']]
        fig = px.line(x=blitz.groupby("end_time")["my_rating"].mean().keys(), y=blitz.groupby("end_time")["my_rating"].mean().values, markers=True,line_shape='hv',color=blitz['result'])
        fig.update_layout(title_text="Rapid rating timeseries based on result", xaxis={'title':'date and time'}, yaxis={'title':'rapid rating'})
        return fig
    elif col_chosen=='blitz-timeseries':
        blitz = mychess_games_df[mychess_games_df['time_class']=='blitz'][['end_time','my_rating','result']]
        fig = px.line(x=blitz.groupby("end_time")["my_rating"].mean().keys(), y=blitz.groupby("end_time")["my_rating"].mean().values, markers=True,line_shape='hv',color=blitz['result'])
        fig.update_layout(title_text="blitz rating timeseries based on result", xaxis={'title':'date and time'}, yaxis={'title':'blitz rating'})
        return fig
    
    elif col_chosen=='world-map':
        country_count = mychess_games_df.groupby(['country']).agg({'pgn':'count'}).reset_index()
        country_count = country_count.rename(columns={'pgn':'player counts'})
        fig = px.choropleth(country_count, 
                    locations='country', 
                    locationmode='country names', 
                    color='player counts', 
                    color_continuous_scale='Blues',
                    range_color=[0, 600])
        fig.update_layout(title_text="My Opponents country distribution")
        return fig
    elif col_chosen=='white-cap-dist':
        r_fig = px.histogram(mychess_games_df[mychess_games_df['my_colour']=='white'], x = "captured_black_pieces_count")
        r_fig.update_layout(height=400,width=600,title='Distribution of me capturing black pieces playing as white',xaxis={'title':'black pieces captured in a single game'},yaxis={'title':'game count'})
        return r_fig
    
    elif col_chosen=='black-cap-dist':
        r_fig = px.histogram(mychess_games_df[mychess_games_df['my_colour']=='black'], x = "captured_white_pieces_count")
        r_fig.update_layout(height=400,width=600,title='Distribution of me capturing white pieces playing as black',xaxis={'title':'black pieces captured in a single game'},yaxis={'title':'game count'})
        return r_fig
    elif col_chosen =='game-stats':
        fig = make_subplots(rows=1, cols=3,  specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=blitz_result,values=blitz_total, title="Blitz"),1,1)
        fig.add_trace(go.Pie(labels=bullet_result,values=bullet_total, title="Bullet"),1,2)
        fig.add_trace(go.Pie(labels=rapid_result,values=rapid_total, title="Rapid"),1,3)
        fig.update_layout(title_text="Win-lose ratio for different time class")
        return fig
    elif col_chosen=='time-per-move':
        fig = go.Figure()
        data = mychess_games_df[mychess_games_df['white_avg_time_per_move']>0]

        fig.add_trace(go.Box(y=data[data['time_class']=='rapid']['rating_class'],
                            x=data[data['time_class']=='rapid']['white_avg_time_per_move'],
                            name='rapid',marker_color='green'))

        fig.add_trace(go.Box(
        y=data[data['time_class']=='blitz']['rating_class'],
        x=data[data['time_class']=='blitz']['white_avg_time_per_move'],
        name='blitz',
        marker_color='yellow'
        ))

        fig.add_trace(go.Box(
        y=data[data['time_class']=='bullet']['rating_class'],
        x=data[data['time_class']=='bullet']['white_avg_time_per_move'],
        name='bullet',
        marker_color='blue'
        ))

        fig.update_layout(boxmode='group',title='Rating class vs average time/move',xaxis={'title':'average time/move'},yaxis={'title':'rating class'})
        fig.update_traces(orientation='h')
        return fig

    else:
        blitz = mychess_games_df[['end_time','my_rating','time_class']]
        fig = px.line(x=blitz.groupby("end_time")["my_rating"].mean().keys(), y=blitz.groupby("end_time")["my_rating"].mean().values, markers=True,line_shape='hv',color=blitz['time_class'])
        fig.update_layout(title_text="rapid vs blitz vs bullet", xaxis={'title':'date and time'}, yaxis={'title':'rating'})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()
