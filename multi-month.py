#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:10:53 2019

@author: madeline
"""

import pandas as pd
import numpy as np
import operator
import plotly as py
#import plotly.graph_objs as go
py.tools.set_credentials_file(username='madelinelee', api_key='FW2B67yKVADiMx2Ahz5G')
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

from datetime import datetime
from datetime import timedelta
from datetime import date

'''user_input = ''
user_input = input('Please enter a pathname for your file, or DONE when done: ')
compare_list = []
compare_count = 0
month_list = []

while user_input != 'DONE':
    user_input = input('Please enter a pathname for your file, or DONE when done: ')
    if user_input == 'DONE':
        if compare_count < 3:
            print('Must input at least 3 files to compare... Try again.')
        
        else:
            print(compare_list)
        
    elif user_input[:-3] == '.csv':
        compare_list.append(user_input)
    
    else:
        print('Error: input is not in right format (must have .csv as suffix!) Try again.')'''

month_dictionary = {1: 'January',
                    2: 'February',
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October',
                    11: 'November',
                    12: 'December'}

def validate_dataframe(data_frame, master_attributes):
    attributes = data_frame.columns.tolist()
    attributes = sorted(attributes)
    
    if attributes != master_attributes:
        print('Error: csv formatted incorrectly - headers do not match')

def prep_data_frame(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    data_frame['year'] = np.nan
    data_frame['month'] = np.nan
    data_frame['day'] = np.nan
    #print(data_frame.shape[0])
    
    for i in range(0, data_frame.shape[0]):
        temp = data_frame['date'].iloc[[i]].astype(datetime)
        #print(temp)
        time_1 = datetime(year = temp.dt.year, month=temp.dt.month, day=temp.dt.day)
        #print('month: ' , time_1.month)
        data_frame['month'][i] = time_1.month
        data_frame['year'][i] = time_1.year
        data_frame['day'][i] = time_1.day
        
    
    #data_frame = data_frame[~data_frame.index.duplicated()]
    
    return(data_frame)
        
    
def get_months(data_frame):
    month_list = []
    month_list = data_frame['month'].unique().tolist()
    
    return(month_list)

def create_master_dataframe(pathname_list):
    print(pathname_list)
    df_list = []
    for pathname in pathname_list:
        temp_dataframe = pd.read_csv(pathname)
        df_list.append(temp_dataframe)
    
    final_frame = pd.concat(df_list).reset_index(drop=True)
    
    return(final_frame)

def get_total_sales(data_frame):
    return(data_frame['sales price'].sum())

def get_mean_sales(data_frame):
    return(data_frame['sales price'].mean())
    
def create_product_sales_dict(data_frame):
    products = data_frame['product'].unique().tolist()
    product_subtotals = {}
    
    for item in products:
        product_subset = data_frame[data_frame['product'] == item]
        product_total = product_subset['sales price'].sum()
        product_subtotals[item] = product_total
        
        sorted_product_subtotals = sorted(product_subtotals.items(), key = operator.itemgetter(1))
        product_subtotals = dict(reversed(sorted_product_subtotals))
    
    return(product_subtotals)
  
def create_comparison_bar(data_frame):
    #this only works if the months are distinct
    #need to figure out year and month 
    month_list = data_frame['month'].unique().tolist()
    month_name = []
    total_month_sales = []
    for month in month_list:
        temp_frame = data_frame[data_frame['month'] == month]
        temp_sales = get_total_sales(temp_frame)
        total_month_sales.append(temp_sales)
        month_name.append(month_dictionary[month])
    
    #print(month_name, total_month_sales)
    
    data = [go.Bar(
            x=month_name,
            y=total_month_sales
    )]
    layout = go.Layout(title='Sales Per Month',
                   xaxis = dict(title='Month'),
                   yaxis = dict(title='Total Sales ($)')
                   )
    figure = go.Figure(data = data,layout=layout)

    py.plot(figure, filename='compare-bar')

#function adapted from previous project i completed on NFL historical data
def create_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','aliceblue','lightgoldenrodyellow']
    products = data_frame['product'].unique().tolist()
    products=sorted(products)
    print(products)
    
    data_list = []
    
    
    
    for i in range(0, len(products)):
        temp_frame = data_frame[data_frame['product'] == products[i]]
        
        temp_scatter = go.Scatter(x=temp_frame['date'],
                              y=temp_frame['sales price'],
                              name= products[i],
                              line=dict(color=colors[i])
                                        )
        data_list.append(temp_scatter)
    
    updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Brown Boots',
                 method = 'update',
                 args = [{'visible': [True, False, False, False, 
                                      False, False, False, False]},
                         {'title': 'Brown Boots Sales over Time ($)',
                          'annotations': []}]
                         ),
            dict(label = 'Button-Down Shirt',
                 method = 'update',
                 args = [{'visible': [False,True, False,False,
                                      False, False, False, False]},
                         {'title': 'Button-Down Shirt Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Khaki Pants',
                 method = 'update',
                 args = [{'visible': [False, False,True, False,
                                      False, False, False, False]},
                         {'title': 'Khaki Pants Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Sticker Pack',
                 method = 'update',
                 args = [{'visible': [False, False, False, True,
                                      False, False, False, False]},
                         {'title': 'Sticker Pack Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Hoodie',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      True, False, False, False]},
                         {'title': 'Super Soft Hoodie Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Sweater',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, True, False, False]},
                         {'title': 'Super Soft Sweater Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Vintage Logo Tee',
             method = 'update',
             args = [{'visible': [False, False, False, False,
                                  False, False, True, False]},
                     {'title': 'Vintage Logo Tee Sales over Time ($)',
                      'annotations': []}]),
            dict(label = 'Winter Hat',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, False, False, True]},
                         {'title': 'Winter Hat Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True,
                                      True, True, True, True]},
                         {'title': 'All Sales over Time ($)',
                          'annotations': []}])
            ]),
        )
    ])
    
    layout = dict(title='Sales vs Time Per Product',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Time'
                        ),
                  yaxis=dict(
                        title = 'Sales ($)'
                        ),                    
                updatemenus=updatemenus)

    fig = dict(data=data_list, layout=layout)
    py.iplot(fig, filename='sales-vs-time-int')


def create_average_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrod']
    products = data_frame['product'].unique().tolist()
    month_list = data_frame['month'].unique().tolist()
    
    products=sorted(products)
    #print(products)
    
    data_list = []
    
    
    for i in range(0, len(products)):
        x_list = []
        y_list = []
        temp_frame = data_frame[data_frame['product'] == products[i]]
        for month in month_list:
            x_list.append(month_dictionary[month])
            temp_month_frame = temp_frame[temp_frame['month'] == month]
            y_list.append(get_mean_sales(temp_month_frame))
        
        
        #print(x_list, y_list)
        
        #print(colors[i])
        temp_scatter = go.Scatter(x=x_list,
                              y=y_list,
                              name= products[i],
                              line=dict(color=colors[i])
                                        )
        
        data_list.append(temp_scatter)
    
    updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Brown Boots',
                 method = 'update',
                 args = [{'visible': [True, False, False, False, 
                                      False, False, False, False]},
                         {'title': 'Brown Boots Sales over Time ($)',
                          'annotations': []}]
                         ),
            dict(label = 'Button-Down Shirt',
                 method = 'update',
                 args = [{'visible': [False,True, False,False,
                                      False, False, False, False]},
                         {'title': 'Button-Down Shirt Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Khaki Pants',
                 method = 'update',
                 args = [{'visible': [False, False,True, False,
                                      False, False, False, False]},
                         {'title': 'Khaki Pants Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Sticker Pack',
                 method = 'update',
                 args = [{'visible': [False, False, False, True,
                                      False, False, False, False]},
                         {'title': 'Sticker Pack Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Hoodie',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      True, False, False, False]},
                         {'title': 'Super Soft Hoodie Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Sweater',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, True, False, False]},
                         {'title': 'Super Soft Sweater Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Vintage Logo Tee',
             method = 'update',
             args = [{'visible': [False, False, False, False,
                                  False, False, True, False]},
                     {'title': 'Vintage Logo Tee Sales over Time ($)',
                      'annotations': []}]),
            dict(label = 'Winter Hat',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, False, False, True]},
                         {'title': 'Winter Hat Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True,
                                      True, True, True, True]},
                         {'title': 'All Sales over Time ($)',
                          'annotations': []}])
            ]),
        )
    ])
    
    layout = dict(title=' Mean Sales vs Month Per Product',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Time (Months)'
                        ),
                  yaxis=dict(
                        title = 'Sales ($)'
                        ),                    
                updatemenus=updatemenus)

    fig = dict(data=data_list, layout=layout)
    py.iplot(fig, filename='mean-sales-vs-month-int')

def create_total_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrod']
    products = data_frame['product'].unique().tolist()
    month_list = data_frame['month'].unique().tolist()
    
    products=sorted(products)
    #print(products)
    
    data_list = []
    
    
    for i in range(0, len(products)):
        x_list = []
        y_list = []
        temp_frame = data_frame[data_frame['product'] == products[i]]
        for month in month_list:
            x_list.append(month_dictionary[month])
            temp_month_frame = temp_frame[temp_frame['month'] == month]
            y_list.append(get_total_sales(temp_month_frame))
        
        
        #print(x_list, y_list)
        
        #print(colors[i])
        temp_scatter = go.Scatter(x=x_list,
                              y=y_list,
                              name= products[i],
                              line=dict(color=colors[i])
                                        )
        
        data_list.append(temp_scatter)
    
    updatemenus = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Brown Boots',
                 method = 'update',
                 args = [{'visible': [True, False, False, False, 
                                      False, False, False, False]},
                         {'title': 'Brown Boots Sales over Time ($)',
                          'annotations': []}]
                         ),
            dict(label = 'Button-Down Shirt',
                 method = 'update',
                 args = [{'visible': [False,True, False,False,
                                      False, False, False, False]},
                         {'title': 'Button-Down Shirt Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Khaki Pants',
                 method = 'update',
                 args = [{'visible': [False, False,True, False,
                                      False, False, False, False]},
                         {'title': 'Khaki Pants Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Sticker Pack',
                 method = 'update',
                 args = [{'visible': [False, False, False, True,
                                      False, False, False, False]},
                         {'title': 'Sticker Pack Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Hoodie',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      True, False, False, False]},
                         {'title': 'Super Soft Hoodie Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Super Soft Sweater',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, True, False, False]},
                         {'title': 'Super Soft Sweater Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'Vintage Logo Tee',
             method = 'update',
             args = [{'visible': [False, False, False, False,
                                  False, False, True, False]},
                     {'title': 'Vintage Logo Tee Sales over Time ($)',
                      'annotations': []}]),
            dict(label = 'Winter Hat',
                 method = 'update',
                 args = [{'visible': [False, False, False, False,
                                      False, False, False, True]},
                         {'title': 'Winter Hat Sales over Time ($)',
                          'annotations': []}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True,
                                      True, True, True, True]},
                         {'title': 'All Sales over Time ($)',
                          'annotations': []}])
            ]),
        )
    ])
    
    layout = dict(title=' Sales vs Month Per Product',
                  showlegend=False,
                  xaxis=dict(
                        title = 'Time (Months)'
                        ),
                  yaxis=dict(
                        title = 'Sales ($)'
                        ),                    
                updatemenus=updatemenus)

    fig = dict(data=data_list, layout=layout)
    py.iplot(fig, filename='sales-vs-month-int')     
    

def month_rank(data_frame):
    total_sales_dict = {}
    month_list = data_frame['month'].unique().tolist()
    
    for month in month_list:
        temp_frame = data_frame[data_frame['month'] == month]
        total_sales_dict[month] = get_total_sales(temp_frame)
    
    total_sales_dict = dict(reversed(sorted(total_sales_dict.items(), key=operator.itemgetter(1))))
    
    for info in total_sales_dict:
        print(month_dictionary[info] + ': ' + "${0:,.2f}".format(total_sales_dict[info]))
    
    return(total_sales_dict)  


        
month_1 = '/Users/madeline/Desktop/SPRING_2019/OPIM_243/sales-reporting-exercise/data/sales-201710.csv'
month_2 = '/Users/madeline/Desktop/sales-201711.csv'
month_3 = '/Users/madeline/Desktop/sales-201712.csv'

test_pathname_list = [month_1, month_2, month_3]
test_frame = create_master_dataframe(test_pathname_list)
test_frame_2 = prep_data_frame(test_frame)
create_line_graph(test_frame_2)
create_comparison_bar(test_frame_2)
print('Months with Highest Sales: ')
month_rank = month_rank(test_frame_2)
create_total_line_graph(test_frame_2)
create_average_line_graph(test_frame_2)


    
