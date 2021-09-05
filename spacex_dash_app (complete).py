# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',
                                options=[{'value': x, 'label': x}
                                        for x in ['ALL', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']],
                                value='ALL',
                                placeholder='Select a launch site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min= 0,
                                max= 10000,
                                step= 1000,
                                value=[min_payload, max_payload],
                                marks= {
                                    0: '0 Kg',
                                    2500: '2500 Kg',
                                    5000: '5000 Kg',
                                    7500: '7500 Kg',
                                    10000: '10000 Kg'

                                }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value')]
)

def show_pie(site):
    
    if site == 'ALL':
        ##"would like to first see which one has the largest SUCCESS COUNT"
        dff_all = spacex_df[(spacex_df['class'] == 1)]
        title_all_pie= f"Total Successful Launches By Site"
        fig = px.pie(
        data_frame=dff_all,
        names='Launch Site',
        values='class',
        title= title_all_pie
        )
        return fig

    else:
        dff_site = spacex_df[spacex_df['Launch Site']==site]
        dff_site_class = dff_site.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        title_site_pie= f"Successful (1) versus Unsucessful (0) Launches for Site {site}"
        fig = px.pie(
        data_frame=dff_site_class,
        names='class',
        values='class count',
        title= title_site_pie
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)

def show_scatter(site, slider):
    low, high = slider
    #slide = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    dfx= spacex_df[spacex_df['Payload Mass (kg)'].between(low, high)]

    if site == 'ALL':
        ##"display all values for variable 'Payload Mass (kg)' and variable 'class'.
        title_all_scatter= f"Payload and Launch Outcome - ALL Launch Sites"
        scatter_fig = px.scatter(
        data_frame=dfx,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title= title_all_scatter
        )
        return scatter_fig

    else:
        dfx_site = dfx[dfx['Launch Site']==site]
        title_site_scatter= f"Payload and Launch Outcome - Launch Site {site}"
        scatter_fig = px.scatter(
        data_frame=dfx_site,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title= title_site_scatter
        )
        return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
