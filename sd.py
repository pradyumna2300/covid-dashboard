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
import plotly.express as px
import requests
#from IPython.core.display import display, HTML
import dash_bootstrap_components as dbc

from settings import config, about
from python.data import Data
from python.model import Model
from python.result import Result




#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']










death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')





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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#def bubble_chart(10):
fig = px.scatter(sorted_country_df.head(20), x="country", y="confirmed", size="confirmed", color="country",
               hover_name="country", size_max=60)
fig.update_layout(
    title=str(10) +" Worst hit countries",
    xaxis_title="Countries",
    yaxis_title="Confirmed Cases",
    width = 10,
    clickmode='event+select'
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

    
        

#interact(bubble_chart, n=10)



#https://codepen.io/chriddyp/pen/bWLwgP.css


# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("logo.PNG"), height="40px")),
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
        children='CovidDash Board',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
     html.Div(children='The time is: ' + str(datetime.datetime.now()), style={
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
    html.H6('The time is: ' + str(datetime.datetime.now()))
    
    
] ),
        
  dcc.Tab(label='Tab three', children=[
           dbc.Container(fluid=True, children=[
    ## Top
    html.H1(config.name, id="nav-pills"),
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
            dbc.Col(html.H4("Forecast 30 days from today"), width={"size":6,"offset":3}), 
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
])
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
        html.H4(country),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("Total cases until today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(total_cases_until_today), style={"color":"white"}),
            
            html.H6("Total cases in 30 days:", className="text-danger"),
            html.H3("{:,.0f}".format(total_cases_in_30days), className="text-danger"),
            
            html.H6("Active cases today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(active_cases_today), style={"color":"white"}),
            
            html.H6("Active cases in 30 days:", className="text-danger"),
            html.H3("{:,.0f}".format(active_cases_in_30days), className="text-danger"),
            
            html.H6("Peak day:", style={"color":peak_color}),
            html.H3(peak_day.strftime("%Y-%m-%d"), style={"color":peak_color}),
            html.H6("with {:,.0f} cases".format(num_max), style={"color":peak_color})
        
        ])
    ])
    return panel

if __name__ == '__main__':
    app.run_server(debug=True)
