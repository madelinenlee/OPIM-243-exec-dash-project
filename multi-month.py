#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:10:53 2019

@author: madeline
"""

import pandas as pd
import numpy
import operator
import plotly as py
import plotly.graph_objs as go

user_input = ''
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
        print('Error: input is not in right format (must have .csv as suffix!) Try again.')

def validate_dataframe(data_frame, master_attributes):
    attributes = data_frame.columns.tolist()
    attributes = sorted(attributes)
    
    if attributes != master_attributes:
        print('Error: csv formatted incorrectly - headers do not match')
        
 
def get_months(pathname_list):
    month_list = []
    for pathname in pathname_list:
        temp_dataframe = pd.read_csv(pathname)
        month = temp_dataframe['date'][0].strftime('%B')
        month_list.append(month)
    
    return(month_list)

def create_master_dataframe(pathname_list):
    df_list = []
    for pathname in pathname_list:
        temp_dataframe = pd.read_csv(pathname)
        df_list.append(temp_dataframe)
    
    final_frame = pd.concat(df_list)
    return(final_frame)

def get_total_sales(data_frame):
    return(data_frame['sales price'].sum())
    
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
    

#function adapted from previous project i completed on NFL historical data
def create_line_graph(data_frame):
    colors = ['#33CFA5','orange','#F06A6A','blue', 'violet',
              'yellowgreen','aliceblue','lightgoldenrodyellow']
    products = data_frame['products'].unique().tolist()
    
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
            dict(label = 'QB',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]},
                         {'title': 'QB Pass Yards (Yards) vs Humidity (%)',
                          'annotations': []}]
                         ),
            dict(label = 'WR',
                 method = 'update',
                 args = [{'visible': [False,True, False,False]},
                         {'title': 'WR Receiving Yards (Yards) vs Humidity (%)',
                          'annotations': []}]),
            dict(label = 'K',
                 method = 'update',
                 args = [{'visible': [False, False,True, False]},
                         {'title': 'K Field Goal Percentage (%) vs Humidity (%)',
                          'annotations': []}]),
            dict(label = 'RB',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]},
                         {'title': 'RB Rush Yards (Yards)',
                          'annotations': []}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True]},
                         {'title': 'Position Metrics vs Humidity (%)',
                          'annotations': []}]),
            dict(label = 'Reset',
                 method = 'update',
                 args = [{'visible': [True, True, True, True]},
                         {'title': 'Position Metrics vs Humidity (%)',
                          'annotations': []}])
            ]),
        )
    ])
        
        
        
    
    
