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
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                            options = [
                                                {'label': 'All Site', 'value': 'All'},
                                                {'label': 'CCAFS LC-40', 'value': 'LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'SLC-40'}
                                            ],
                                            placeholder = 'Select a Launch Site here',
                                            searchable = True                                
                                ),),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0, max = 10000, step = 1000,
                                                value=[
                                                    spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All' or entered_site is None:
        pie_data = (spacex_df.groupby('Launch Site')['class'].sum())/(spacex_df['class'].sum())
        pie_data = pd.DataFrame(pie_data)
        pie_data.reset_index(inplace = True)
        pie_data.rename(columns={'class': 'success rate'}, inplace= True)
        fig = px.pie(pie_data, names='Launch Site', values='success rate',
                     title='Total successful launches count for all sites ')
        return fig
    else:
        #Preparing data for pie chart of each data
        success_rate_each_launch = (spacex_df.groupby('Launch Site')['class'].mean())*100
        success_rate_each_launch = pd.DataFrame(success_rate_each_launch)
        success_rate_each_launch.rename(columns = {'class': 'Success rate'}, inplace=True)
        success_rate_each_launch['Fail rate'] = 100 - success_rate_each_launch['Success rate']
        labels_name = ['Success rate', 'Fail rate']

        if entered_site == 'LC-40':
            data_LC_40 = success_rate_each_launch.loc['CCAFS LC-40']
            fig_LC_40 = px.pie(names = labels_name, values = list(data_LC_40[i] for i in labels_name),
                            title='Total Launch for site CCAFS LC-40')
            return fig_LC_40
    
        if entered_site == 'SLC-4E':
            data_SLC_4E = success_rate_each_launch.loc['VAFB SLC-4E']
            fig_SLC_4E = px.pie(names=labels_name, values=list(data_SLC_4E[i] for i in labels_name),
                               title='Total Launch for site VAFB SLC-4E')
            return fig_SLC_4E

        if entered_site == 'LC-39A':
            data_LC_39A = success_rate_each_launch.loc['KSC LC-39A']
            fig_LC_39A = px.pie(names=labels_name, values=list(data_LC_39A[i] for i in labels_name),
                                title='Total Launch for site KSC LC-39A')
            return fig_LC_39A
    
        if entered_site == 'SLC-40':
            data_SLC_40 = success_rate_each_launch.loc['CCAFS SLC-40']
            fig_SLC_40 = px.pie(names=labels_name, values=list(data_SLC_40[i] for i in labels_name),
                            title='Total Launch for site CCAFS SLC-40')
            return fig_SLC_40
        
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id= 'site-dropdown', component_property = 'value'), Input(component_id='payload-slider', component_property= 'value')]
    )
def get_scatter_chart(entered_site, entered_range):
    filtered_dataframe = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_range[0]]
    filtered_dataframe = filtered_dataframe[filtered_dataframe['Payload Mass (kg)'] <= entered_range[1]]

    if entered_site == 'All' or entered_site is None:
        chart = px.scatter(filtered_dataframe, 
                            x='Payload Mass (kg)', 
                            y='class', 
                            color='Booster Version Category',
                            title = 'Correlation between Payload and Success for all sites')
        return chart

    if entered_site == 'LC-40':
        data_LC_40 = filtered_dataframe[filtered_dataframe['Launch Site'] == 'CCAFS LC-40']
        chart = px.scatter(data_LC_40,
                           x='Payload Mass (kg)',
                           y='class',
                           color='Booster Version Category',
                           title='Correlation between Payload and Success for CCAFS LC-40')
        return chart

    if entered_site == 'SLC-4E':
        data_SLC_4E = filtered_dataframe[filtered_dataframe['Launch Site'] == 'VAFB SLC-4E']
        chart = px.scatter(data_SLC_4E,
                           x='Payload Mass (kg)',
                           y='class',
                           color='Booster Version Category',
                           title='Correlation between Payload and Success for VAFB SLC-4E')
        return chart
    
    if entered_site == 'LC-39A':
        data_LC_39A = filtered_dataframe[filtered_dataframe['Launch Site'] == 'KSC LC-39A']
        chart = px.scatter(data_LC_39A,
                           x='Payload Mass (kg)',
                           y='class',
                           color='Booster Version Category',
                           title='Correlation between Payload and Success for VAFB SLC-4E')
        return chart

    if entered_site == 'SLC-40':
        data_SLC_40 = filtered_dataframe[filtered_dataframe['Launch Site'] == 'CCAFS SLC-40']
        chart = px.scatter(data_SLC_40,
                           x='Payload Mass (kg)',
                           y='class',
                           color='Booster Version Category',
                           title='Correlation between Payload and Success for VAFB SLC-4E')
        return chart

# Run the app
if __name__ == '__main__':
    app.run_server()

