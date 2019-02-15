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

#user_input = ''
#user_input = input('Please enter a pathname for your file, or DONE when done: ')
#compare_list = []
#month_list = []

#function to load in pathnames
def user_input():
    user_input = ''
    compare_list = []
    month_list = []
    while user_input != 'DONE':
        user_input = input('Please enter a pathname for your file, or DONE when done: ')
        if user_input == 'DONE':
            return(compare_list)
    
        elif user_input[-4:] == '.csv':
            compare_list.append(user_input)
        
        else:
            print('Error: input is not in right format (must have .csv as suffix!) Try again.')

master_attributes = ['date', 'product', 'unit price', 'units sold', 'sales price']
master_attributes = sorted(master_attributes)

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

#function to validate dataframe based on attributes
def validate_dataframe(data_frame, master_attributes):
    attributes = data_frame.columns.tolist()
    attributes = sorted(attributes)
    
    if attributes != master_attributes:
        print('Error: csv formatted incorrectly - headers do not match')
        return(False)
    elif attributes == master_attributes:
        return(True)

#function to  prep the dataframe by loading in datetime 
def prep_data_frame(data_frame):
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    data_frame['year'] = np.nan
    data_frame['month'] = np.nan
    data_frame['month-year'] = np.nan
    #print(data_frame.shape[0])
    for i in range(0, data_frame.shape[0]):
        temp = data_frame['date'].iloc[[i]].astype(datetime)
        #print(temp)
        time_1 = datetime(year = temp.dt.year, month=temp.dt.month, day=temp.dt.day)
        #print('month: ' , time_1.month)
        data_frame['month'][i] = time_1.month
        data_frame['year'][i] = time_1.year
        data_frame['month-year'][i] = str(time_1.month) + '-' + str(time_1.year)
        
    
    #data_frame = data_frame[~data_frame.index.duplicated()]
    
    return(data_frame)

#function to get list of months        
def get_months(data_frame):
    month_list = []
    month_list = data_frame['month'].unique().tolist() 
    
    return(month_list)

#function to get list of unique keys
def get_key_list(data_frame):
    unique_key_list = data_frame['month-year'].unique().tolist()
    return(unique_key_list)
    
#create dataframe from list of csvs to load in     
def create_master_dataframe(pathname_list):
    print(pathname_list)
    df_list = []
    for pathname in pathname_list:
        temp_dataframe = pd.read_csv(pathname)
        df_list.append(temp_dataframe)
    
    final_frame = pd.concat(df_list).reset_index(drop=True)
    
    return(final_frame)

#function to return total sales
def get_total_sales(data_frame):
    return(data_frame['sales price'].sum())

#fucntion to return mean sales
def get_mean_sales(data_frame):
    return(data_frame['sales price'].mean())

#function to create product dictionary, ranked descending     
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
 
#function to create bar chart to compare total sales per month
def create_comparison_bar(data_frame):
    #this only works if the months are distinct
    #need to figure out year and month 
    month_year_list = data_frame['month-year'].unique().tolist()
    month_year_list = sorted(month_year_list)
    #print(month_year_list)
    month_name = []
    total_month_sales = []
    for key in month_year_list:
        #print(key)
        temp_frame = data_frame[data_frame['month-year'] == key]
        
        #print(month_dictionary[temp_frame['month'][0]])
        
        temp_sales = get_total_sales(temp_frame)
        
        total_month_sales.append(temp_sales)
        
        month_name.append(key)
    
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

#line graph functions adapted from previous project i completed on NFL historical data
    
#function to create line graph of sales over time per each product, interactive
def create_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrodyellow']
    products = data_frame['product'].unique().tolist()
    products=sorted(products)
    #print(products)
    
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


#function to create average sales of each product per month, interactive
def create_average_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrod']
    
    products = data_frame['product'].unique().tolist()
    month_year_list = data_frame['month-year'].unique().tolist()
    
    month_year_list = sorted(month_year_list)
    
    products=sorted(products)
    #print(products)
    
    data_list = []
    
    
    for i in range(0, len(products)):
        x_list = []
        y_list = []
        temp_frame = data_frame[data_frame['product'] == products[i]]
        for key in month_year_list:
            temp_month_frame = temp_frame[temp_frame['month-year'] == key]
            x_list.append(key)
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

#function to create total sales per month, interactive plot
def create_total_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','darkgrey','goldenrod']
    products = data_frame['product'].unique().tolist()
    month_year_list = data_frame['month-year'].unique().tolist()
    
    month_year_list = sorted(month_year_list)
    
    products=sorted(products)
    #print(products)
    
    data_list = []
    
    
    for i in range(0, len(products)):
        x_list = []
        y_list = []
        temp_frame = data_frame[data_frame['product'] == products[i]]
        for key in month_year_list:
            temp_month_frame = temp_frame[temp_frame['month-year'] == key]
            x_list.append(key)
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
    
    layout = dict(title='Total Sales vs Month Per Product',
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
    

#function to make dictionary with months and total sales, sorted descending
def month_rank(data_frame):
    total_sales_dict = {}
    month_year_list = data_frame['month-year'].unique().tolist()
    
    for key in month_year_list:
        temp_frame = data_frame[data_frame['month-year'] == key]
        month = temp_frame['month'].unique().tolist()
        total_sales_dict[month_dictionary[month[0]]] = get_total_sales(temp_frame)
    
    total_sales_dict = dict(reversed(sorted(total_sales_dict.items(), key=operator.itemgetter(1))))
    
    for info in total_sales_dict:
        #print(info)
        #print(total_sales_dict[info])
        print(info + ': ' + "${0:,.2f}".format(float(total_sales_dict[info])))
    
    return(total_sales_dict)  

#function to make dictionary with months and total sales, sorted ascending
def low_sales(data_frame):
    total_sales_dict = {}
    month_year_list = data_frame['month-year'].unique().tolist()
    
    for key in month_year_list:
        temp_frame = data_frame[data_frame['month-year'] == key]
        month = temp_frame['month'].unique().tolist()
        total_sales_dict[month_dictionary[month[0]]] = get_total_sales(temp_frame)
    
    total_sales_dict = dict(sorted(total_sales_dict.items(), key=operator.itemgetter(1)))
    
    for info in total_sales_dict:
        #print(info)
        #print(total_sales_dict[info])
        print(info + ': ' + "${0:,.2f}".format(float(total_sales_dict[info])))
    
    return(total_sales_dict)  

#month_1 = '/Users/madeline/Desktop/SPRING_2019/OPIM_243/sales-reporting-exercise/data/sales-201710.csv'
#month_2 = '/Users/madeline/Desktop/sales-201711.csv'
#month_3 = '/Users/madeline/Desktop/sales-201712.csv'

#test_pathname_list = [month_1, month_2, month_3]
#test_frame = create_master_dataframe(test_pathname_list)

def final_run():
    test_pathname_list = user_input()
    test_frame = create_master_dataframe(test_pathname_list)
    if validate_dataframe(test_frame, master_attributes) == True:
        test_frame_2 = prep_data_frame(test_frame)
        create_line_graph(test_frame_2)
        print('see your line graph of sales per product over time at https://plot.ly/~madelinelee/65/sales-vs-time-per-product/#/')
        create_comparison_bar(test_frame_2)
        print('see your bar chart comparing total sales per month at https://plot.ly/~madelinelee/69/sales-per-month/#/')
        create_total_line_graph(test_frame_2)
        print('see your product vs total sales per month at https://plot.ly/~madelinelee/71/sales-vs-month-per-product/#/')
        create_average_line_graph(test_frame_2)
        print('see your product vs mean sales per month at https://plot.ly/~madelinelee/73/mean-sales-vs-month-per-product/#/')
        print('Month Ranking, Highest Sales: ')
        month_rank_dict = month_rank(test_frame_2)
    else:
        print('Please try again...')
    
final_run()
    
