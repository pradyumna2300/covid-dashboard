import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import pycountry
import plotly.express as px
import requests
#from IPython.core.display import display, HTML
import dash_bootstrap_components as dbc

from settings import config, about
from python.data import Data
from python.model import Model
from python.result import Result

import dash_table




#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']










death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
a=df.drop(df.index[[0,0]], inplace=True)



# data cleaning

# renaming the df column names to lowercase
country_df.columns = map(str.lower, country_df.columns)
confirmed_df.columns = map(str.lower, confirmed_df.columns)
death_df.columns = map(str.lower, death_df.columns)
recovered_df.columns = map(str.lower, recovered_df.columns)

# changing province/state to state and country/region to country
confirmed_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
recovered_df = confirmed_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
death_df = death_df.rename(columns={'province/state': 'state', 'country/region': 'country'})
country_df = country_df.rename(columns={'country_region': 'country'})
# country_df.head()

# total number of confirmed, death and recovered cases
confirmed_total = int(country_df['confirmed'].sum())
deaths_total = int(country_df['deaths'].sum())
recovered_total = int(country_df['recovered'].sum())
active_total = int(country_df['active'].sum())

sorted_country_df = country_df.sort_values('confirmed', ascending= False)

# Read data
data = Data()
data.get_data()





external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(name=config.name, assets_folder=config.root+"/application/static/log.png", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name

BUTTON_STYLE = {
    'margin': '25px'
}


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#################india####
# print(df)
# Adding new columns for fatality and survival ratio
df['Fatality Rate %'] = round(df['Deaths'].astype(float) * 100 / df['Confirmed'], 2)
df['Survival Rate %'] = round(df['Recovered'].astype(float) * 100 / df['Confirmed'], 2)

# Calculate KPIs here
#df=df.drop(df.index[[0,0]], inplace=True) 
states_effected =len(df)

confirmed = df['Confirmed'].sum()
cured = df['Recovered'].sum()
deaths = df['Deaths'].sum()

recovered_perc = round(float(cured * 100 / confirmed),2)
serious = confirmed - cured - deaths
fatality_ratio = round(float(deaths * 100 / confirmed), 2)

state_most_cases = df[df['Confirmed'] == df['Confirmed'].max()]
state_kpi1 = state_most_cases['State'] + " " + str(state_most_cases['Confirmed'].values)

state_most_cured = df[df['Recovered'] == df['Recovered'].max()]

# If more than one state have same number of cured cases, pick one with `higher Survival Rate %`
if len(state_most_cured.index) > 1:
    state_most_cured = state_most_cured[state_most_cured['Survival Rate %'] == state_most_cured['Survival Rate %'].max()]

state_kpi2 = state_most_cured['State'] + " " + str(state_most_cured['Recovered'].values)
# print(df)

#def bubble_chart(10):
fig = px.scatter(sorted_country_df.head(20), x="country", y="confirmed", size="confirmed", color="country",
               hover_name="country", size_max=60)
fig.update_layout(
    title=str(10) +" Worst hit countries",
    xaxis_title="Countries",
    yaxis_title="Confirmed Cases",
    width = 10,
    clickmode='event+select'
    #paper_bgcolor="lightgrey",
    #plot_bgcolor=colors['background'],
    #paper_bgcolor=colors['background'],
    #font_color=colors['text']
    )
fig.add_annotation( align='right')
    #fig.show();

    #fig.show();
    
a=px.bar(
    sorted_country_df.head(10),
    x = "country",
    y = "deaths",
    title= "Top 10 worst affected countries", # the axis names
   # color_discrete_sequence=["pink"], 
    height=500,
    width=800
)    
a.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
b=px.bar(
    sorted_country_df.head(10),
    x = "country",
    y = "recovered",
    title= "Top 10 worst affected countries", # the axis names
   # color_discrete_sequence=["pink"], 
    height=500,
    width=800
)

b.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
b.add_annotation( align='right')

## map##
df1 = pd.read_csv(URL_DATASET)
# print(df1.head) # Uncomment to see what the dataframe is like
# ----------- Step 2 ------------
list_countries = df1['Country'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

# print(d_country_code) # Uncomment to check dictionary  

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v

# print(df1.head)  # Uncomment to confirm that ISO codes added
# ----------- Step 3 ------------
#MAP#
m = px.choropleth(data_frame = df1, 
                    locations= "iso_alpha",
                    color= "Confirmed",  # value in column 'Confirmed' determines color
                    hover_name= "Country",
                    color_continuous_scale= 'RdYlGn',  #  color scale red, yellow green
                    animation_frame= "Date")

    
        

#interact(bubble_chart, n=10)



#https://codepen.io/chriddyp/pen/bWLwgP.css


# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("log.PNG"), height="100px")),
    ## about
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", id="about-popover", active=False),
        dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            dbc.PopoverHeader("How it works"), dbc.PopoverBody(about.txt)
        ])
    ])),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contacts"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])


# Input
inputs = dbc.FormGroup([
    html.H4("Select Country"),
    dcc.Dropdown(id="country", options=[{"label":x,"value":x} for x in data.countrylist], value="World")
]) 


app.layout =  html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
        children='Covid Dash Board',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    #html.Div(children='Dash: A web application framework for Python.', style={
        #'textAlign': 'center',
        #'color': colors['text']
   # }),
    
     html.Div(children='The time is: ' + str(datetime.datetime.now()), style={
        'textAlign': 'left',
        'color': colors['text']
    }),
    
    
     html.Div(children='CONFIRMED: ' + str(confirmed_total) , style={
        'textAlign': 'left',
        'color': colors['text']
    }),
     html.Div(children='DEATHS: ' + str(deaths_total), style={
        'textAlign': 'left',
        'color': colors['text']
    }),
     html.Div(children='RECOVERED: ' + str(recovered_total), style={
        'textAlign': 'left',
        'color': colors['text']
    }),

     html.Div([
     dcc.Tabs([
        dcc.Tab(label='Tab one', children=[


        
                                                                                           
      
    
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    ),
    
    dcc.Graph(
        id='life',
        figure=a
    ),
    
    dcc.Graph(
        id='recover',
        figure=b
    ),
    dcc.Graph(
                id='map', figure=m
            ),       
    html.H6('The time is: ' + str(datetime.datetime.now()))
    
    
] ),
 # dcc.Tabs([
      #html.Br(),html.Br(),html.Br(),
        dcc.Tab(label='CovidIndia', children=[
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                ],
                data=df.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=30,
                style_header={'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'fontSize': 14, 'font-family': 'sans-serif', 'width': 'auto'}
            ),
            
             #dcc.Tab(label='Bar-Graphs', children=[
            dcc.Loading(
                id="loading-icon",
                children=[
                    html.Div(id='datatable-interactivity-container')
                ],
                type="circle"
            ),
                 
            html.Div([
                dcc.Interval(id='interval1', interval=1000, n_intervals=-1000),
                html.H1(id='label1', children='')
            ]),
            html.Br(),
            dbc.Button(
                ["Confirmed Cases", dbc.Badge(confirmed, color="light", className="ml-1 h1")],
                color="dark", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["Serious", dbc.Badge(serious, color="light", className="ml-1 h1")],
                color="warning", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["Recovered Cases",
                 dbc.Badge(str(cured) + " (" + str(recovered_perc) + "%)", color="light", className="ml-1 h1")],
                color="success", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["Deaths", dbc.Badge(deaths, color="light", className="ml-1 h1")],
                color="danger", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["Fatality Ratio", dbc.Badge(str(fatality_ratio) + "%", color="light", className="ml-1 h1")],
                color="primary", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["States/UT Effected", dbc.Badge(str(states_effected) + " / 36", color="light", className="ml-1 h1")],
                color="secondary", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["States/UT Most Cases", dbc.Badge(state_kpi1, color="light", className="ml-1 h1")],
                color="warning", style=BUTTON_STYLE),
            html.Br(),
            dbc.Button(
                ["States/UT Most Cured", dbc.Badge(state_kpi2, color="light", className="ml-1 h1")],
                color="success", style=BUTTON_STYLE)
        ])     
            
        ]),
        
        
       
        
     dcc.Tab(label='NEXT', children=[
           dbc.Container(fluid=True, children=[
    ## Top
    #html.H1(config.name, id="nav-pills"),
    navbar,
    html.Br(),html.Br(),html.Br(),

    ## Body
    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            inputs, 
            html.Br(),html.Br(),html.Br(),
            html.Div(id="output-panel")
        ]),
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("World covid data"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="plot-total"), label="Total cases"),
                dbc.Tab(dcc.Graph(id="plot-active"), label="Active cases")
            ])
        ])
    ])
])
        ]),                                                                                         
                                                                                           
        
                                                                                           
       
        ])
])
#])

#@app.callback(Output("loading-icon", "children"))

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
   
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["State"],
                        "y": dff[column],
                        "type": "bar",
                        "text": dff[column],
                        "textposition": 'auto',
                        "marker": {"color": colors},
                        "hoverinfo": 'skip'
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                    },
                    "title": {
                        "text": column,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    "height": 250,
                    "margin": {"t": 20, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["Confirmed", "Recovered", "Deaths"] if
        column in dff
    ]


# Python functions for about navitem-popover
@app.callback(output=Output("about","is_open"), inputs=[Input("about-popover","n_clicks")], state=[State("about","is_open")])
def about_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(output=Output("about-popover","active"), inputs=[Input("about-popover","n_clicks")], state=[State("about-popover","active")])
def about_active(n, active):
    if n:
        return not active
    return active



# Python function to plot total cases
@app.callback(output=Output("plot-total","figure"), inputs=[Input("country","value")]) 
def plot_total_cases(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    return result.plot_total(model.today)



# Python function to plot active cases
@app.callback(output=Output("plot-active","figure"), inputs=[Input("country","value")])
def plot_active_cases(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    return result.plot_active(model.today)
    

    
# Python function to render output panel
@app.callback(output=Output("output-panel","children"), inputs=[Input("country","value")])
def render_output_panel(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    peak_day, num_max, total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days = result.get_panel()
    peak_color = "white" if model.today > peak_day else "red"
    panel = html.Div([
        html.H4(country ,style={"color":"white"}),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("Total cases until today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(total_cases_until_today), style={"color":"white"}),
            
            #html.H6("Total cases in 30 days:", className="text-danger"),
            #html.H3("{:,.0f}".format(total_cases_in_30days), className="text-danger"),
            
            html.H6("Active cases today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(active_cases_today), style={"color":"white"}),
            
            #html.H6("Active cases in 30 days:", className="text-danger"),
            #html.H3("{:,.0f}".format(active_cases_in_30days), className="text-danger"),
            
            #html.H6("Peak day:", style={"color":peak_color}),
            #html.H3(peak_day.strftime("%Y-%m-%d"), style={"color":peak_color}),
           # html.H6("with {:,.0f} cases".format(num_max), style={"color":peak_color})
        
        ])
    ])
    return panel

#if __name__ == '__main__':
 #   app.run_server(debug=True)
