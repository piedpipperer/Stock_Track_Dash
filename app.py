# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 18:23:35 2019

@author: JORDI
"""

#pip install iexfinance 

import dash
import dash_core_components as dcc
import dash_html_components as html
#import iexfinance
from dash.dependencies import Output, Input, State



#from iexfinance.stocks import get_historical_data
#from iexfinance.altdata import get_social_sentiment
#get_social_sentiment("TSLA", token = IEX_Token)
#from iexfinance.stocks import Stock
#tesla = Stock(symbols="TSLA"
#                        , token = IEX_Token)



#from datetime
import datetime as dt
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np




from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt




#import http.client
#conn = http.client.HTTPSConnection("api.iextrading.com", timeout=15)
#		conn.request('GET', '/1.0/' + api_data)
#		response = conn.getresponse().read().decode('utf-8')
#		data = json.loads(response)
#api(f'stock/{symbol}/news')




from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
import requests

#import os

#print(update_news())



#scraping newssss
import bs4
from bs4 import BeautifulSoup

#
##url = "https://seekingalpha.com/symbol/"
#url = "https://finance.yahoo.com/quote/"
#url_2 = "?ltr=1"
#ticker = "TSLA"
#
#r= requests.get(url+ticker+url_2
#                )
#soup = bs4.BeautifulSoup(r.text,"xml")
#
#soup.find_all('<a')
#find_all('target=href')
#="/m


#import pandas_datareader.data as web
#web.get_data_yahoo("TSLA")






#from urllib.request import urlopen as uReq
#    uClient = uReq(url+ticker , proxies={'http':'105.19.49.178:80'
#                                })




def update_news(input_value="TSLA"):
    
    url_base = "https://seekingalpha.com/"
    
    ticker = "symbol/" + input_value
    r = requests.get(url_base+ticker#'https://seekingalpha.com/symbol/AMAT/earnings'
                     , proxies={'http':'50.207.31.221:80'}
                     #, proxies={'http':'105.19.49.178:80'   }
                             
                     ).text
    
    soup = bs4.BeautifulSoup(r, 'html.parser' 
                             #,"xml"
                             )
    
    test = soup.find_all('a',
                  {#'class':'symbol_article'
                   #,
                   'sasource':'portfolio_focused'
                  
                   } #, format = 'dataframe'
                          )#[0]
    
    test2 = soup.find_all('a',
                  {#'class':'symbol_article'
                   #,
                   'sasource':'qp_latest'
                  
                   } #, format = 'dataframe'
                          )#[0]


#    type(test)
#    test[0].text
#    test[0].get('href')
    df = pd.DataFrame(
  columns=['headline', 'new'])

    headlines = []
    news = []
    #df["headline"] = test[0].text
    if len(test) >= 1:  
        i = 0

        while (i < len(test)):
            headlines.append(test[i].text)
            news.append(url_base+test[i].get('href')[1:])
  #can it be included in one line?
            i += 2
            

    df['headline'] = headlines
    df['new'] = news
    df['type'] = "analysis"



    df2 = pd.DataFrame(
  columns=['headline', 'new'])

    headlines = []
    news = []
    #df["headline"] = test[0].text
    if len(test2) >= 1:  
        i = 0

        while (i < len(test2)):
            headlines.append(test2[i].text)
            news.append(url_base+test2[i].get('href')[1:])
  #can it be included in one line?
            i += 1
            

    df2['headline'] = headlines
    df2['new'] = news
    df2['type'] = "news"
    
    #now need to rbind both dataframes and return.
    
    
    return  pd.concat([df,df2], axis = 0)

# pd.concat([df,df2], axis = 0).head()
    
#process to include something in dash: 

#df = get_historical_data("GE",start=start, end=end, output_format="pandas"
#                         ,token=IEX_Token)
#trace_close = go.Scatter(x=list(df.index),
#                         y=list(df.close),
#                         name="Close",
#                         line=dict(color="#f44242"))
#
#layout = dict(tictle="Stock Chart",showlegend=False)
                                   




app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server


app.layout = html.Div( 
                    className="row",
                    children=[html.Div(#className="row",
                       html.H1(children="Stock Monitor")),
              
        html.Div([ dcc.Input(id="stock-input", value="GE", type="text")
                  ,html.Button(id="submit-stock-button",n_clicks=0,children="Submit")
        ])
              
        ,html.Div(style = {"display":"flex"}
            ,children=[
                # Column for user controls
                html.Div(className="column"
                         ,style={"width": "49.75%"}
                         ,children=[
                        dcc.Graph(id="Stock_Chart"
#                                  ,figure={"data":[trace_close]
#                                  ,"layout": { "title":"Stock Evol"}
#                                  }
                        )]
                    )
                ,
                html.Div(className="column"
                         ,style={"width": "49.75%"}
                         ,children=[#call generate function
                      html.H3("Seeking Alpha News")
#                      ,generate_html_table(1,input_value)
                      ,     html.Div(id='my-div') 
                       ]
                    ) 
                 ]
)
]
)
                
# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
# we should put our token here 

    
    
@app.callback(dash.dependencies.Output("my-div", component_property='children'),
              #PENDING to include the other div.
              [dash.dependencies.Input("submit-stock-button", "n_clicks")],
              [State("stock-input","value")]       
             )
def update_html_table(n_clicks=1#, max_rows=5
                        , input_value="TSLA"):
    max_rows=5
    #input_value="TSLA"

    df = update_news(input_value)
    
    df_analysis = df[(df.type=='analysis')]
    df_news = df[(df.type=='news')]

    
    trace_close =     html.Div(
#        [
                html.Table(#id="news",
                    # Header
                    [html.Tr([html.Th("Analyses"),html.Th("News")])]
                    +
                    # Body
                    [
                        html.Tr(
                            children=[
                                html.Td(
                                    html.A(
                                        df_analysis["headline"][i],
                                        href=df_analysis["new"][i],
                                        target="_blank"
                                    )
                                )
                                 ,html.Td(
                                    html.A(
                                        df_news["headline"][i],
                                        href=df_news["new"][i],
                                        target="_blank"
                                    )
                                )
#                                ,html.Td(
#                                    html.A(
#                                        df[(df.type=='new')]["headline"][i],
#                                        href=df[(df.type=='new')]["new"][i],
#                                        target="_blank"
#                                    )
#                                )    
                            ]
                        )
                        for i in range(min(len(df_analysis),max_rows))
                    ]#
                ),
                style={"height": "300px", "overflowY": "scroll"}
            )
#        ,],
#        style={"height": "100%"}#,id="news"
#        )
                    
#    data.append(trace_close)         
    
#    layout = {"title": input_value}                    
    
    return trace_close
#    return {"data": input_value, #data, 
#            "layout": data
#            }                    


#
#
@app.callback(dash.dependencies.Output("Stock_Chart", "figure"),
              #PENDING to include the other div.
              [dash.dependencies.Input("submit-stock-button", "n_clicks")],
              [State("stock-input","value")]       
             )
def update_fig(n_clicks=1, input_value="TSLA"):
    #input_value = "TSLA"
    #input_value = "PEPE"
    #falta el update news!!!
    
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&datatype=csv&symbol=" 
    #ticker (input VALUE)
    url_2 = "&apikey="
    alpha_vantage_key = "AJ667WPIEISWAOZG"

    
    start = dt.datetime.today() - relativedelta(years=1#months=6 
                             )
    end = dt.datetime.today()
    #update_news(input_value)
    #ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')

    try:
        df0 = pd.read_csv(url+input_value+url_2+alpha_vantage_key
                          ,parse_dates=["timestamp"] 
                          ,date_parser=lambda x: pd.to_datetime(x, format='%Y/%m/%d')
                          )
    except:
        #long_description = 'Python module to get stock data from the Alpha Vantage Api'
        return {"data": [], 
            "layout": dict(title="Could not read from API")
            }
 
        
    #filter last 3years
    df = df0[df0.timestamp >= (start)]
    #IEX_Token = "pk_b5d1c9d30db24c6eb746cdace5e97242"
    
    #hem de posar el api aquest del advantage
#    df = get_historical_data(input_value,start=start, end=end, output_format="pandas"
#                         ,token=IEX_Token)

    data = []
    
    trace_close = go.Scatter(x=list(df.timestamp),
                             y=list(df.close),
                             name="Close",
                              line=dict(color="#f44242"))
    data.append(trace_close)         
    
    layout = dict(title=input_value,
                  autosize=False,
                  xaxis=dict(
                            rangeselector=dict(
                                    buttons=list([
                                                dict(count=1,
                                                     label="1w",
                                                     step="week",
                                                     stepmode="backward"),
                                                dict(count=1,
                                                     label="1m",
                                                     step="month",
                                                     stepmode="backward"),
                                                dict(count=6,
                                                     label="6m",
                                                     step="month",
                                                     stepmode="backward"),
                                                dict(count=1,
                                                     label="YTD",
                                                     step="year",
                                                     stepmode="todate")
#                                                ,   dict(count=1,
#                                                     label="1y",
#                                                     step="year",
#                                                     stepmode="backward")
                                                ,
                                            dict(step="all")
                                                    ])
                                            ),
                            rangeslider=dict(
                                visible=True
                                            )
#                            ,type="date"
                            ) 
                )                    
    
    return {"data": data, 
            "layout": layout
            }                    
                        
                        
if __name__ == "__main__":
    app.run_server(debug=True
                   )