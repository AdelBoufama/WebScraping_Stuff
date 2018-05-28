# -*- coding: utf-8 -*-
import csv
import StringIO
import requests
import pdb
import pandas as pd
import numpy
from bs4 import BeautifulSoup, SoupStrainer
import itertools
from itertools import izip_longest

df = pd.read_csv('data.csv')
df = df[pd.notnull(df['Address'])]
df = df[pd.notnull(df['Main_Phone_Number']) | pd.notnull(df['Secondary_Number'])]
df.to_csv('data2.csv', index=False, encoding='utf8') #output without index value and force to encoding to utf8
