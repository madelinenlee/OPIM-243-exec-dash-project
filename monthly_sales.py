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

user_input = '/Users/madeline/Desktop/SPRING_2019/OPIM_243/sales-reporting-exercise/data/sales-201710.csv'
#input('please input the file pathname to load: ')

sales_data = pd.read_csv(user_input)


