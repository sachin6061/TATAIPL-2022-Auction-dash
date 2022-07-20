from dash import Dash, html, dcc, dash_table, Output, Input, callback
import pandas as pd
import plotly.graph_objects as go
from dash_iconify import DashIconify

ipl = pd.read_csv('ipl_2022_dataset.csv')
ipl.reset_index(drop=True, inplace=True)
ipl.drop_duplicates(inplace=True)
ipl.drop('Cost IN $ (000)', axis=1, inplace=True)
# ipl.rename({'COST IN ?? (CR.)': 'COST IN CR.'}, inplace=True)
total_plr = ipl.groupby(by='TYPE')['Player'].count()
t_plr = len(ipl['Player'].unique())
t_all_rounder = total_plr['ALL-ROUNDER']
t_batter = total_plr['BATTER']
t_bowler = total_plr['BOWLER']
t_wicketkeeper = total_plr['WICKETKEEPER']
sold_players = ipl.loc[ipl['Team'] != 'Unsold']
t_sold = sold_players['Player'].count()
sold_plr = sold_players.groupby(by='TYPE')['Player'].count()
s_all_rounder = sold_plr['ALL-ROUNDER']
s_batter = sold_plr['BATTER']
s_bowler = sold_plr['BOWLER']
s_wicketkeeper = sold_plr['WICKETKEEPER']
cost = sold_players['COST IN ?? (CR.)'].sum()
teams = sold_players['Team'].unique()

Investments_of_each_team = sold_players.groupby(by='Team')['COST IN ?? (CR.)'].sum()
labels = list(Investments_of_each_team.to_dict().keys())
values = list(Investments_of_each_team.to_dict().values())

overall = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='value+percent',
                                 insidetextorientation='radial', hole=.4
                                 )])
overall.update_layout(
    title={
        'text': "Investment OF Each Team IN CR.",
        'y': 0.9,
        'x': 0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='#e0ebeb')


@callback(
    [Output("datatable", "data"), Output('datatable', 'columns'), Output('exp-Batter', 'children'),
     Output('exp-Bowler', 'children'), Output('exp-Keeper', 'children'), Output('exp-All-Rounder', 'children'),
     Output("pie_chart", "figure"), Output("bar_chart", "figure")],
    Input('sel_tem', 'value')

)
def fnSelTeam(team):
    team_df = ipl.loc[ipl['Team'] == team]

    exp_btter_df = team_df.loc[team_df['TYPE'] == 'BATTER']
    exp_bttr = \
        exp_btter_df[exp_btter_df['COST IN ?? (CR.)'] == exp_btter_df['COST IN ?? (CR.)'].max()].to_dict("records")[0]
    exp_bttr = str('Name - ' + exp_bttr['Player'] + ', Cost In CR. - ' + str(exp_bttr['COST IN ?? (CR.)']))

    exp_bolr_df = team_df.loc[team_df['TYPE'] == 'BOWLER']
    exp_bolr = \
        exp_bolr_df[exp_bolr_df['COST IN ?? (CR.)'] == exp_bolr_df['COST IN ?? (CR.)'].max()].to_dict("records")[0]
    exp_bolr = str('Name - ' + exp_bolr['Player'] + ', Cost In CR. - ' + str(exp_bolr['COST IN ?? (CR.)']))

    exp_keeper_df = team_df.loc[team_df['TYPE'] == 'WICKETKEEPER']
    exp_kpr = \
        exp_keeper_df[exp_keeper_df['COST IN ?? (CR.)'] == exp_keeper_df['COST IN ?? (CR.)'].max()].to_dict("records")[
            0]
    exp_kpr = str('Name - ' + exp_kpr['Player'] + ', Cost In CR. - ' + str(exp_kpr['COST IN ?? (CR.)']))

    exp_rounder_df = team_df.loc[team_df['TYPE'] == 'ALL-ROUNDER']
    exp_rounder = \
        exp_rounder_df[exp_rounder_df['COST IN ?? (CR.)'] == exp_rounder_df['COST IN ?? (CR.)'].max()].to_dict(
            "records")[
            0]
    exp_rounder = str('Name - ' + exp_rounder['Player'] + ', Cost In CR. - ' + str(exp_rounder['COST IN ?? (CR.)']))

    sum_cost = team_df.groupby(by='TYPE')['COST IN ?? (CR.)'].sum()
    sum_lbl = list(sum_cost.to_dict().keys())
    sum_val = list(sum_cost.to_dict().values())

    total_grpby = team_df.groupby(by='TYPE')['Player'].count()
    labels = list(total_grpby.to_dict().keys())
    values = list(total_grpby.to_dict().values())

    bar = go.Figure(data=[go.Bar(x=sum_lbl, y=sum_val, text=sum_val, textposition='auto', name='cost'),
                          go.Bar(x=labels, y=values, text=values, textposition='auto', name='No of Players'), ])
    # bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    bar.update_layout(
        barmode='group',
        title={
            'text': "Total Players in IPL 2022",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis=dict(
            title='Cost IN CR.',
            titlefont_size=16,
            tickfont_size=14,
        ),
        paper_bgcolor='#e0ebeb'
    )

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='value+label+percent',
                                 insidetextorientation='radial', hole=.4
                                 )])
    fig.update_layout(
        title={
            'text': "Total Team Cost",
            'y': 0.9,
            'x': 0.45,
            'xanchor': 'center',
            'yanchor': 'top'},
        paper_bgcolor='#e0ebeb')

    data = team_df.to_dict("records")
    return data, [{"name": i, "id": i} for i in team_df.columns], exp_bttr, exp_bolr, exp_kpr, exp_rounder, fig, bar


app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.Div(html.H1('TATA IPL 2022'),className='main-header'),
    html.Div([html.Div([html.Div(
        [DashIconify(icon="noto:cricket-game", width=50, height=50), html.Label('Total Players ' + str(t_plr))],
        className='lbl1 lbl'),
        html.Div([DashIconify(icon="noto-v1:cricket-game", width=50, height=50),
                  html.Label('Total Batter ' + str(t_batter))], className='lbl2 lbl'),
        html.Div([DashIconify(icon="bx:cricket-ball", width=50, height=50),
                  html.Label('total Bowlers ' + str(t_bowler))], className='lbl3 lbl'),
        html.Div([DashIconify(icon="twemoji:gloves", width=50, height=50),
                  html.Label('Total Wicket Keepers ' + str(t_wicketkeeper))], className='lbl4 lbl'),
        html.Div([DashIconify(icon="maki:cricket", width=50, height=50),
                  html.Label('Total All-rounder ' + str(t_all_rounder))], className='lbl5 lbl')],
        className='upper'),
        html.Div([html.Div([DashIconify(icon="noto:cricket-game", width=30, height=30),
                            html.Label('Sold Players ' + str(t_sold))], className='lbl1 lbl'),
                  html.Div([DashIconify(icon="noto-v1:cricket-game", width=30, height=30),
                            html.Label('Sold Batter ' + str(s_batter))], className='lbl2 lbl'),
                  html.Div([DashIconify(icon="bx:cricket-ball", width=30, height=30),
                            html.Label('Sold Bowlers ' + str(s_bowler))], className='lbl3 lbl'),
                  html.Div([DashIconify(icon="twemoji:gloves", width=30, height=30),
                            html.Label('Sold Wicket Keepers ' + str(s_wicketkeeper))], className='lbl4 lbl'),
                  html.Div([DashIconify(icon="maki:cricket", width=30, height=30),
                            html.Label('Sold All-rounder ' + str(s_all_rounder))], className='lbl5 lbl'),
                  html.Div([DashIconify(icon="emojione:money-bag", width=30, height=30),
                            html.Label('Total COST IN Team Building ' + '{:.2f}'.format(cost)+' CR.')], className='lbl lbl')],
                 className='lower')],
        className='header'),
    html.Div([html.Div([html.H4('Select Team'),
                        dcc.Dropdown(teams, id='sel_tem', value=teams[0], className='dropdown')],
                       className='div-drpdwn'),
              html.Div(
                  [html.Div([html.H2('Expensive Batsman'),
                             html.H4(id='exp-Batter')], className='lbl'),
                   html.Div([html.H2('Expensive Bowler'),
                             html.H4(id='exp-Bowler')], className='lbl'),
                   html.Div([html.H2('Expensive Wicket-Keeper'),
                             html.H4(id='exp-Keeper')], className='lbl'),
                   html.Div([html.H2('Expensive All Rounder'),
                             html.H4('bhumra', id='exp-All-Rounder')], className='lbl')
                   ], className='card')], className='drp-down'),
    html.Div([
        html.Div(dcc.Graph(id='bar_chart'), className='left-main'),
        html.Div(dcc.Graph(id='pie_chart'), className='right-main')], className='main'),

    html.Div([html.Div(dash_table.DataTable(
        id='datatable',
        style_table={
            'overflowY': 'scroll',
            'overflowX': 'scroll',
        },
        page_size=14,
        style_cell={'textAlign': 'center', 'background-color': '#e0ebeb', 'color': 'black'},
        style_header={'textAlign': 'center', 'background-color': '#85adad', "font-size": "1vw", 'color': 'white'},
        style_as_list_view=True,
        tooltip_delay=0,
        tooltip_duration=None, page_action='native'
    ), className='tbl left-main'), html.Div(dcc.Graph(id='total_chart', figure=overall), className='right-main')],
        className='sub-header')
])

if __name__ == '__main__':
    app.run_server()
