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

nameList = ['Company_Name']
numberList = ['Main_Phone_Number']
phone2List = ['Secondary_Number']
ratingList = ['Rating']
addressList =['Address']
postalCodeList = ['Postal_Code']
mapsUrlList = ['Google Map Url']

data = [nameList,numberList,phone2List,ratingList,addressList,postalCodeList, mapsUrlList]

def scrapeMainPage(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})

    pageNum = 0
    while g_data is not None:
        pageNum = pageNum + 1
        print url[:-12] + str(pageNum) + "&AreaID=416"
        r = requests.get(url[:-12] + str(pageNum) + "&AreaID=416")
        soup = BeautifulSoup(r.content)
        g_data = soup.find("table",{"id":"ctl00_cphRight_Main0102view_1_DataList1"})
        if g_data is None:
            break

        names = g_data.find_all("a",{"class":"tree12"})
        contacts = g_data.find_all("span",{"class":"T12"})
        hyperLinks = g_data.find_all("a")

        for name in names:
            name = name.text.encode('utf8')
            nameList.append(name)

        for link in hyperLinks:
            locationData = scrapeInnerPage(url[0:20] + link["href"])
            phone2List.append(locationData[0])
            addressList.append(locationData[1])
            postalCodeList.append(locationData[2])
            mapsUrlList.append(locationData[3])


        for item in g_data:
            try:
                phoneNum = item.contents[1].find_all("span",{"class":"T12"})[1].text.encode('utf8')
                if phoneNum[-12:][0:3] == '416' or phoneNum[-12:][0:3] == '647' or phoneNum[-12:][0:5] == '437' or phoneNum[-12:][0:3] == '1-8':
                    numberList.append(phoneNum[-12:])
                else:
                    numberList.append('N/A')
            except:
                pass

        for item in g_data:
            try:
                rating = item.contents[1].find_all("span",{"class":"T12"})[2].text.encode('utf8')
                ratingList.append(rating[30:len(rating)])
            except:
                pass
        #print data


def scrapeInnerPage(url):
    r2 = requests.get(url)
    soup2 = BeautifulSoup(r2.content)
    phoneNum2 = soup2.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkPhone2"})
    addressData = soup2.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkAddress"})
    addressDataM = soup2.find("span",{"id":"ctl00_cphLeft_Viewms1_txtLinkAddress"})
    postalCodeData = soup2.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkPostalCode"})
    postalCodeDataM = soup2.find("span",{"id":"ctl00_cphLeft_Viewms1_txtLinkPostalCode"})
    mapData = soup2.find("span",{"id":"ctl00_cphLeft_Views1_txtLinkMap"})
    mapDataM = soup2.find("span",{"id":"ctl00_cphLeft_Viewms1_txtLinkMap"})

    if phoneNum2 is not None:
        if phoneNum2.text.encode('utf8')[0:3] == '416' or phoneNum2.text.encode('utf8')[0:3] == '647' or phoneNum2.text.encode('utf8')[0:3] == '437' or phoneNum2.text.encode('utf8')[0:3] == '1-8':
            phoneNums = phoneNum2.text.encode('utf8')
        else:
            phoneNums = 'N/A'
    else:
        phoneNums = 'N/A'

    if addressData is not None:
        address = addressData.text.encode('utf8')
    elif addressDataM is not None:
        address = addressDataM.text.encode('utf8')
    else:
        address = 'N/A'

    if postalCodeData is not None:
        postalCode = postalCodeData.text.encode('utf8')
    elif postalCodeDataM is not None:
        postalCode = postalCodeDataM.text.encode('utf8')
    else:
        postalCode = 'N/A'

    if mapData is not None:
        mapsUrl = mapData.find('a')['href'].encode('utf8')

    elif mapDataM is not None:
        mapsUrl = mapDataM.find('a')['href'].encode('utf8')
    else:
        mapsUrl = 'N/A'


    return [phoneNums, address, postalCode, mapsUrl]



def scrapeOuterPage(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    entryNum =0
    while 0 <= entryNum <= 7:
        if entryNum < 10:
            dataPiece = soup.find("span",{"id":"ctl00_cphRight_Main0102s_1_dlTree_ctl0" + str(entryNum) + "_Label1"})
        else:
            dataPiece = soup.find("span",{"id":"ctl00_cphRight_Main0102s_1_dlTree_ctl" + str(entryNum) + "_Label1"})

        link = dataPiece.find('a')
        headerName = link.text.encode('utf8')
        print headerName

        nameList.append(headerName)
        numberList.append(headerName)
        phone2List.append(headerName)
        ratingList.append(headerName)
        addressList.append(headerName)
        postalCodeList.append(headerName)
        mapsUrlList.append(headerName)

        innerLink = "http://www.cn411.ca/" + link['href'] + "&PageSize=100&PageID=1&AreaID=416"

        scrapeMainPage(innerLink)
        entryNum = entryNum + 1

scrapeOuterPage\
("http://www.cn411.ca/main02s04.aspx?&LinkTreeID=S0203")


#scrapeMainPage\
#("http://www.cn411.ca/main02view04.aspx?LinkTreeID=S020517&PageSize=100&PageID=1&AreaID=416")

with open('data.csv','a') as file: #This writes to csv on every page when in the while loop
    writer = csv.writer(file)
    export_data = izip_longest(*data) #need to learn what izip_longest() does...
    writer.writerows(export_data)
