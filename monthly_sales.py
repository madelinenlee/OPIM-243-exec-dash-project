#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 18:10:35 2019

@author: madeline
"""

import pandas as pd
import operator
import numpy as np
import os
from collections import OrderedDict
import plotly as py
import plotly.graph_objs as go

py.tools.set_credentials_file(username='madelinelee', api_key='FW2B67yKVADiMx2Ahz5G')
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF


#test pathname 
#pathname = '/Users/madeline/Desktop/SPRING_2019/OPIM_243/sales-reporting-exercise/data/sales-201710.csv'
attributes = ['date', 'product','unit price', 'units sold', 'sales price']


#from starter code https://github.com/s2t2/exec-dash-starter-py/commit/525446a5850d211bb78dfe1cb3ffb42ea4b3c9ad
def to_usd(price):
    return '${0:, .2f}'.format(price)


#adapted from sales reporting exercise https://github.com/madelinenlee/OPIM-243-sales-reporting-exercise/blob/master/sales_reporting.py
user_input = input('please input the file pathname to load: ')
sales_data = pd.read_csv(user_input)

#error checking, but only once
if sales_data.columns.tolist() != attributes:
    print('Oops: csv not formatted correctly... are you sure you want to load this in?')
    user_input = input('please input the file pathname to load: ')
    sales_data = pd.read_csv(user_input)

#change date to datetime, initialize variables   
sales_data['date'] = pd.to_datetime(sales_data['date'])
month = sales_data['date'][0].strftime('%B')
year = sales_data['date'][0].strftime('%Y')


print('SALES REPORT ('+ sales_data['date'][0].strftime('%B') +
                     ' ' + sales_data['date'][0].strftime('%Y') +
                     ')')
print('TOTAL SALES : $' + "${0:,.2f}".format(sales_data['sales price'].sum()))
      #str('%0.2f'%sales_data['sales price'].sum()))

products = sales_data['product'].unique().tolist()

product_subtotals = {}


#create product dictionary
for item in products:
    product_subset = sales_data[sales_data['product'] == item]
    product_total = product_subset['sales price'].sum()
    product_subtotals[item] = product_total

sorted_product_subtotals = sorted(product_subtotals.items(), key = operator.itemgetter(1))
product_subtotals = dict(reversed(sorted_product_subtotals))

print('TOP 3 SELLING PRODUCTS: ')

count = 1

for item in product_subtotals:
    temp_float = product_subtotals[item]
    print(str(count) + '. ' + item + ' ' + '${0:,.2f}'.format(temp_float))
    count = count + 1
    if count > 3:
        break

#from https://github.com/madelinenlee/OPIM-243-chart-exercise
x = []
y = []

for item in product_subtotals:
    y.append(item)
    x.append('$' + str(product_subtotals[item]))

x = list(reversed(x))

data = [go.Bar(
            x=x,
            y=y,
            orientation = 'h'
    )]

margin = go.Margin(l = 200, r = 50)

layout = go.Layout(title='Top Selling Products (' + month + ' ' + year + ')',
                   xaxis = dict(title='USD ($)'),
                   yaxis = dict(title='Product'),
                   margin = margin
                   )
figure = go.Figure(data = data,layout=layout)

py.iplot(figure, filename='horizontal-bar.html')
print('see your top selling products for this month at https://plot.ly/~madelinelee/75')
#https://plot.ly/~madelinelee/75

