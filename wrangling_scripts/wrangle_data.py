import pandas as pd
import plotly.graph_objs as go
import io
import requests


def get_data(url):
    """Reads the dataframe from url csv on JHU github page
    
    Args:
        url (str): link to the csv file on github
    
    Returns:
        Dataframe (pd.DataFrame): Dataframe for global COVID19 reports up until now
    """
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    return df

def get_top_ten(df_cases):
    """ Returns top 10 rows in descending order of the sum by the last column, grouped by 'Country/Region' column
    
    Args:
        df_cases (pd.DataFrame): dataframe with corona cases (total, death or recovered)
    Returns:
        list1 with country names, list2 with number of cases, string with name of last column (i.e., the date)
    """
    cases_per_country_df = df_cases.groupby('Country/Region')[df_cases.columns[-1]].sum().reset_index()
    top_10 = cases_per_country_df.sort_values(by=cases_per_country_df.columns[-1], ascending=False).head(10)
    
    x = top_10['Country/Region'].values.tolist()
    current_date = top_10.columns[-1]
    y = top_10[current_date].values.tolist()
    
    return x, y, current_date


def get_top_timeseries(df_cases):
    """Returns time series data for top 10 countries
    
    Args:
        df (pd.DataFrame): dataframe with daily number of cases
        
    Returns:
        list of countries and number of daily cases as time series
    """
    
    cases_per_country_df = df_cases.groupby('Country/Region')[df_cases.columns[4:]].sum().reset_index()
    top_10 = cases_per_country_df.sort_values(by=cases_per_country_df.columns[-1], ascending=False).head(10)
    
    countries = top_10['Country/Region'].values.tolist()
    ys = []
    x = top_10.columns[1:]
    xs = []
    country_names = []
    for el in countries:
        ys.append(top_10[top_10['Country/Region'] == el].values[0][1:].tolist())
        xs.append(x)
    return xs, ys, countries

def get_dynamic_fig():
    # load dataset
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")

    # create figure
    fig = go.Figure()

    # Add surface trace
    fig.add_trace(go.Surface(z=df.values.tolist(), colorscale="Viridis"))

    # Update plot sizing
    fig.update_layout(
        width=800,
        height=900,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template="plotly_white",
    )

    # Update 3D scene options
    fig.update_scenes(
        aspectratio=dict(x=1, y=1, z=0.7),
        aspectmode="manual"
    )

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "surface"],
                        label="3D Surface",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "heatmap"],
                        label="Heatmap",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Trace type:", showarrow=False,
            x=0, y=1.085, yref="paper", align="left")
        ]
    )
    
    return fig



def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # confirmed cases
    url_cases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    df_cases = get_data(url_cases)
    
    # confirmed deaths
    url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    df_deaths = get_data(url_deaths)
    
    url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    df_recovered = get_data(url_recovered)
    
    
    df_cases_focused = df_cases[df_cases['Country/Region'].isin(['Afghanistan', 'Bangladesh'])]
    df_deaths_focused = df_deaths[df_deaths['Country/Region'].isin(['Afghanistan', 'Bangladesh'])]
    df_recovered_focused = df_recovered[df_recovered['Country/Region'].isin(['Afghanistan', 'Bangladesh'])]


    # Bar chart for top 10 countries
    
    graph_one = []
    x, y, current_date = get_top_ten(df_cases)
    graph_one.append(
      go.Bar(
      x = x,
      y = y,
      name = 'Number of Cases'
      )
    )
    
    
    
    

    layout_one = dict(title = 'Top 10 Countries with Highest Number of <br> Cases Until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Cases Until {}'.format(current_date)),
                )

        



# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    x, y, current_date = get_top_ten(df_deaths)
    graph_two.append(
      go.Bar(
      x = x,
      y = y,
      )
    )

    layout_two = dict(title = 'Top 10 Countries with Highest Number of <br> Deaths Until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Deaths Until {}'.format(current_date)),
                )
    

# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    x, y, current_date = get_top_ten(df_recovered)
    graph_three.append(
        go.Bar(
            x = x,
            y = y,
        )
    )
#     graph_three.append(
#       go.Scatter(
#       x = [5, 4, 3, 2, 1, 0],
#       y = [0, 2, 4, 6, 8, 10],
#       mode = 'lines'
#       )
#     )

    layout_three = dict(title = 'Top 10 Countries with Highest Number of <br> Recoveries Until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Recoveries Until {}'.format(current_date)),
                )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    xs, ys, countries = get_top_timeseries(df_cases)
    for x,y,c in zip(xs,ys,countries):
        graph_four.append(
          go.Scatter(
          x = x[-30:],
          y = y[-30:],
          mode = 'lines',
          name = c
          )
        )

    layout_four = dict(title = 'Trend in Number of Cases <br> in the Last 30 Days',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Number of Cases'),
                )
    
    
    
    
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    
    # NEW GRAPHS
    
    graph_one = []
    x, y, current_date = get_top_ten(df_cases_focused)
    graph_one.append(
      go.Bar(
      x = x,
      y = y,
      name = 'Number of Cases'
      )
    )
    
    
    
    

    layout_one = dict(title = 'Number of cases until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Cases Until {}'.format(current_date)),
                )

        



# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    x, y, current_date = get_top_ten(df_deaths_focused)
    graph_two.append(
      go.Bar(
      x = x,
      y = y,
      )
    )

    layout_two = dict(title = 'Number of Deaths Until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Deaths Until {}'.format(current_date)),
                )
    

# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    x, y, current_date = get_top_ten(df_recovered_focused)
    graph_three.append(
        go.Bar(
            x = x,
            y = y,
        )
    )
#     graph_three.append(
#       go.Scatter(
#       x = [5, 4, 3, 2, 1, 0],
#       y = [0, 2, 4, 6, 8, 10],
#       mode = 'lines'
#       )
#     )

    layout_three = dict(title = 'Number of Recoveries Until {}'.format(current_date),
                xaxis = dict(title = 'Countries',),
                yaxis = dict(title = 'Number of Recoveries Until {}'.format(current_date)),
                )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    xs, ys, countries = get_top_timeseries(df_cases_focused)
    for x,y,c in zip(xs,ys,countries):
        graph_four.append(
          go.Scatter(
          x = x[-30:],
          y = y[-30:],
          mode = 'lines',
          name = c
          )
        )

    layout_four = dict(title = 'Trend in Number of Cases <br> in the Last 30 Days',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'Number of Cases'),
                )
    
    
    
    
    
    # append all charts to the figures list
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))


    return figures