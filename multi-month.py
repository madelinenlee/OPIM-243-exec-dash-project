#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:10:53 2019

@author: madeline
"""

import pandas as pd
import numpy
import plotly as py
import plotly.graph_objs as go

user_input = ''
user_input = input('Please enter a pathname for your file, or DONE when done: ')
compare_list = []

month_list = []

while user_input != 'DONE':
    user_input = input('Please enter a pathname for your file, or DONE when done: ')
    
    if user_input == 'DONE':
        print(compare_list)
    
    elif user_input[:-3] == '.csv':
        compare_list.append(user_input)
    else:
        print('Error: input is not in right format (must have .csv as suffix!) Try again.')


        
        
    temp_dataframe = pd.read_csv(user_input)
    month_list.append(temp_dataframe)

