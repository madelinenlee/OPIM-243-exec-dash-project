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
    

for pathname in compare_list:
    temp_dataframe = pd.read_csv(pathname)
    month_list.append(temp_dataframe)

def get_total_sales(data_frame):
    return(data_frame['sales price'].sum())
    
def create_product_sales_dict(data_frame):
    products = sales_data['product'].unique().tolist()
    product_subtotals = {}
    
    for item in products:
        product_subset = sales_data[sales_data['product'] == item]
        product_total = product_subset['sales price'].sum()
        product_subtotals[item] = product_total
        
        
        sorted_product_subtotals = sorted(product_subtotals.items(), key = operator.itemgetter(1))
        product_subtotals = dict(reversed(sorted_product_subtotals))
    
    return(product_subtotals)
