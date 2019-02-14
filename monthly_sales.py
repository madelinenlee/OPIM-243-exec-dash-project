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


pathname = '/Users/madeline/Desktop/SPRING_2019/OPIM_243/sales-reporting-exercise/data/sales-201710.csv'
attributes = ['date', 'product','unit price', 'units sold', 'sales price']


#from starter code https://github.com/s2t2/exec-dash-starter-py/commit/525446a5850d211bb78dfe1cb3ffb42ea4b3c9ad

def to_usd(price):
    return '${0:, .2f}'.format(price)



user_input = input('please input the file pathname to load: ')
sales_data = pd.read_csv(user_input)

if sales_data.columns.tolist() != attributes:
    print('Oops: csv not formatted correctly... are you sure you want to load this in?')

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

x = []
y = []

for item in product_subtotals:
    y.append(item)
    x.append('$' + str(product_subtotals[item]))

x = list(reversed(x))

data = [go.Bar(
            x=x,
            y=y,
            orientation='h'
    )]
layout = go.Layout(title='Top Selling Products (' + month + ' ' + year + ')',
                   xaxis = dict(title='USD'),
                   yaxis = dict(title='Product')
                   )
figure = go.Figure(data = data,layout=layout)

py.offline.plot(figure, filename='horizontal-bar.html', auto_open = True)


