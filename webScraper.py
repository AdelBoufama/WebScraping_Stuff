# -*- coding: utf-8 -*-
import csv
import StringIO
import requests
import pdb
from bs4 import BeautifulSoup
import itertools
from itertools import izip_longest
#from itertools import zip_longest

#url = "http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020131&PageSize=100&PageID=1"
url = "http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020505&PageSize=10&PageID=1"

r = requests.get(url)
soup = BeautifulSoup(r.content)

#pages = soup.find("span",{"id":"ctl00_cphRight_Main0102view_1_lbPager"})
#lastPage = str(pages)[-9:-7]

g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})

pageNum = 0

while g_data is not None:
    pageNum = pageNum + 1
    url = url[:-1] + str(pageNum)
    #url = "http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020131&PageSize=100&PageID=" + str(pageNum)
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})
    if g_data is None:
        break

    names = g_data.find_all("a",{"class":"tree12"})
    contacts = g_data.find_all("span",{"class":"T12"})
    numberList = []
    nameList = []
    ratingList = []
    data = [nameList,numberList,ratingList]

    for name in names:
        # pdb.set_trace()
        name = name.text.encode('utf8')
        nameList.append(name)

    for item in g_data:
        try:
            phoneNum = item.contents[1].find_all("span",{"class":"T12"})[1].text.encode('utf8')
            numberList.append(phoneNum)

        except:
            pass

    for item in g_data:
        try:
            rating = item.contents[1].find_all("span",{"class":"T12"})[2].text.encode('utf8')
            ratingList.append(rating[30:len(rating)])
        except:
            pass

    export_data = izip_longest(*data, fillvalue = '')

    with open('data.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow(("nameList","numberList","ratingList"))
        writer.writerows(export_data)
