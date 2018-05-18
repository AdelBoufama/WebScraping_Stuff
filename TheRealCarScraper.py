# -*- coding: utf-8 -*-
import logging, time, urllib2, StringIO, gzip, re, urlparse, csv, random, os, datetime, sys, getopt, requests, json
from lxml import etree
from urllib2 import urlopen
from urlparse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#import common

logging.basicConfig(level=logging.DEBUG)
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = datetime.datetime.now().strftime("%Y-%m-%d")
csvFileName = dir_path + '/' + filename + '.csv'

csvHeaders = [
    'stockno',
    'vin',
    'seller',
    'name',
    'year',
    'make',
    'model',
    'body_style',
    'transmission',
    'engine',
    'drivetrain',
    'fuel',
    'price',
    'mileage',
    'horsepower',
    'eff_highway',
    'eff_city',
    'description',
    'trim',
    'doors',
    'main_img',
    'thumb_main_img',
    'imgs',
    'thumb_imgs',
    'source_url',
    'ex_color',
    'in_color',
    'proof',
    'cert'
]

def getDataMain(url):
  # payload = "{\"size\":50,\"from\":0,\"query\":{\"filtered\":{\"filter\":{\"bool\":{\"must\":[{\"not\":{\"term\":{\"administration.isSold\":\"1\"}}},{\"bool\":{\"should\":[{\"bool\":{\"must\":[{\"term\":{\"dealer.export_id.lower\":\"3197\"}},{\"term\":{\"dealer.dealership_feed_id.lower\":\"609\"}},{\"term\":{\"filters.condition.lower\":\"certified\"}},{\"bool\":{\"should\":[{\"range\":{\"filters.price.price\":{\"gte\":0}}}]}}]}},{\"bool\":{\"must\":[{\"term\":{\"dealer.export_id.lower\":\"3197\"}},{\"term\":{\"dealer.dealership_feed_id.lower\":\"609\"}},{\"term\":{\"filters.condition.lower\":\"pre-owned\"}},{\"bool\":{\"should\":[{\"range\":{\"filters.price.price\":{\"gte\":0}}}]}}]}},{\"bool\":{\"must\":[{\"term\":{\"dealer.export_id.lower\":\"3197\"}},{\"term\":{\"dealer.dealership_feed_id.lower\":\"609\"}},{\"term\":{\"filters.condition.lower\":\"new\"}},{\"bool\":{\"should\":[{\"range\":{\"filters.price.price\":{\"gte\":0}}}]}}]}}]}},{\"bool\":{\"should\":[{\"term\":{\"filters.condition.lower\":\"certified\"}},{\"term\":{\"filters.condition.lower\":\"pre-owned\"}}]}}]}},\"query\":{\"bool\":{\"should\":[{\"match_all\":{}}]}}}},\"aggregations\":{\"colors\":{\"terms\":{\"field\":\"filters.exteriorColor.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"makes\":{\"terms\":{\"field\":\"filters.make.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"models\":{\"terms\":{\"field\":\"filters.model.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"rawModel\":{\"terms\":{\"field\":\"filters.model\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"byTrim\":{\"terms\":{\"field\":\"filters.trim.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"rawTrim\":{\"terms\":{\"field\":\"filters.trim\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"byMake\":{\"terms\":{\"field\":\"filters.make.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"bodyStyles\":{\"terms\":{\"field\":\"filters.bodyStyle.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"SubbodyStyles\":{\"terms\":{\"field\":\"filters.sub_bodystyle.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"minPrice\":{\"min\":{\"field\":\"filters.price.minPrice\"}},\"maxPrice\":{\"max\":{\"field\":\"filters.price.maxPrice\"}},\"priceBreakdown\":{\"filter\":{\"bool\":{\"must\":[{\"not\":{\"term\":{\"filters.price.maxPrice\":0}}}]}},\"aggregations\":{\"breakdown\":{\"histogram\":{\"field\":\"price\",\"interval\":5000}}}},\"mileageBreakdown\":{\"histogram\":{\"field\":\"filters.mileage\",\"interval\":15000}},\"minYear\":{\"min\":{\"field\":\"filters.year\"}},\"maxYear\":{\"max\":{\"field\":\"filters.year\"}},\"years\":{\"terms\":{\"field\":\"filters.year\",\"size\":0,\"order\":{\"_term\":\"desc\"}}},\"conditions\":{\"terms\":{\"field\":\"filters.condition.lower\"}},\"maxMileage\":{\"max\":{\"field\":\"filters.mileage\"}},\"retailers\":{\"terms\":{\"field\":\"filters.dealer_map_key.lower\",\"include\":\".+\",\"size\":0}},\"transmissions\":{\"terms\":{\"field\":\"filters.transmissionType.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"engines\":{\"terms\":{\"field\":\"filters.engine.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"packages\":{\"terms\":{\"field\":\"filters.packages.lower\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"Custom Field 1\":{\"terms\":{\"field\":\"filters.Custom Field 1.lower\",\"size\":0}},\"Custom Field 2\":{\"terms\":{\"field\":\"filters.Custom Field 2.lower\",\"size\":0}},\"Custom Field 3\":{\"terms\":{\"field\":\"filters.Custom Field 3.lower\",\"size\":0}},\"Custom Field 4\":{\"terms\":{\"field\":\"filters.Custom Field 4.lower\",\"size\":0}},\"Custom Field 5\":{\"terms\":{\"field\":\"filters.Custom Field 5.lower\",\"size\":0}},\"Custom Field 6\":{\"terms\":{\"field\":\"filters.Custom Field 6.lower\",\"size\":0}},\"Custom Field 7\":{\"terms\":{\"field\":\"filters.Custom Field 7.lower\",\"size\":0}},\"Custom Field 8\":{\"terms\":{\"field\":\"filters.Custom Field 8.lower\",\"size\":0}},\"Custom Field 9\":{\"terms\":{\"field\":\"filters.Custom Field 9.lower\",\"size\":0}},\"Custom Field 10\":{\"terms\":{\"field\":\"filters.Custom Field 10.lower\",\"size\":0}}},\"sort\":[{\"date.createdDate\":{\"order\":\"desc\",\"ignore_unmapped\":true}}]}"
  # payload = "{\"size\":50,\"from\":0,\"query\":{\"filtered\":{\"filter\":{\"bool\":{\"must\":[{\"not\":{\"term\":{\"administration.isSold\":\"1\"}}},{\"bool\":{\"should\":[{\"bool\":{\"must\":[{\"term\":{\"dealer.export_id.lower\":\"20150612114443319\"}},{\"term\":{\"dealer.dealership_feed_id.lower\":\"6469\"}},{\"term\":{\"filters.condition.lower\":\"pre-owned\"}},{\"bool\":{\"should\":[{\"range\":{\"filters.price.msrp\":{\"gte\":0}}}]}}]}}]}},{\"bool\":{\"should\":[{\"term\":{\"filters.condition.lower\":\"certified\"}},{\"term\":{\"filters.condition.lower\":\"pre-owned\"}}]}}]}},\"query\":{\"bool\":{\"should\":[{\"match_all\":{}},{\"boosting\":{\"positive\":{\"range\":{\"maxPrice\":{\"gte\":1}}},\"negative\":{\"range\":{\"maxPrice\":{\"lt\":1}}},\"negative_boost\":0.5}}]}}}},\"aggregations\":{\"colors\":{\"terms\":{\"field\":\"filters.exteriorColor.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"makes\":{\"terms\":{\"field\":\"filters.make.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"models\":{\"terms\":{\"field\":\"filters.model.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"rawModel\":{\"terms\":{\"field\":\"filters.model\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"byTrim\":{\"terms\":{\"field\":\"filters.trim.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"rawTrim\":{\"terms\":{\"field\":\"filters.trim\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"byMake\":{\"terms\":{\"field\":\"filters.make.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"bodyStyles\":{\"terms\":{\"field\":\"filters.bodyStyle.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}},\"aggregations\":{\"SubbodyStyles\":{\"terms\":{\"field\":\"filters.sub_bodystyle.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}}}},\"minPrice\":{\"min\":{\"field\":\"filters.price.minPrice\"}},\"maxPrice\":{\"max\":{\"field\":\"filters.price.maxPrice\"}},\"priceBreakdown\":{\"filter\":{\"bool\":{\"must\":[{\"not\":{\"term\":{\"filters.price.maxPrice\":0}}}]}},\"aggregations\":{\"breakdown\":{\"histogram\":{\"field\":\"filters.price.maxPrice\",\"interval\":5000}}}},\"mileageBreakdown\":{\"histogram\":{\"field\":\"filters.mileage\",\"interval\":15000}},\"minYear\":{\"min\":{\"field\":\"filters.year\"}},\"maxYear\":{\"max\":{\"field\":\"filters.year\"}},\"years\":{\"terms\":{\"field\":\"filters.year\",\"size\":0,\"order\":{\"_term\":\"desc\"}}},\"conditions\":{\"terms\":{\"field\":\"filters.condition.lower\"}},\"maxMileage\":{\"max\":{\"field\":\"filters.mileage\"}},\"retailers\":{\"terms\":{\"field\":\"filters.dealer_map_key.lower\",\"include\":\".+\",\"size\":0}},\"transmissions\":{\"terms\":{\"field\":\"filters.transmissionType.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"engines\":{\"terms\":{\"field\":\"filters.engine.lower\",\"include\":\".+\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"packages\":{\"terms\":{\"field\":\"filters.packages.lower\",\"size\":0,\"order\":{\"_term\":\"asc\"}}},\"Custom Field 1\":{\"terms\":{\"field\":\"filters.Custom Field 1.lower\",\"size\":0}},\"Custom Field 2\":{\"terms\":{\"field\":\"filters.Custom Field 2.lower\",\"size\":0}},\"Custom Field 3\":{\"terms\":{\"field\":\"filters.Custom Field 3.lower\",\"size\":0}},\"Custom Field 4\":{\"terms\":{\"field\":\"filters.Custom Field 4.lower\",\"size\":0}},\"Custom Field 5\":{\"terms\":{\"field\":\"filters.Custom Field 5.lower\",\"size\":0}},\"Custom Field 6\":{\"terms\":{\"field\":\"filters.Custom Field 6.lower\",\"size\":0}},\"Custom Field 7\":{\"terms\":{\"field\":\"filters.Custom Field 7.lower\",\"size\":0}},\"Custom Field 8\":{\"terms\":{\"field\":\"filters.Custom Field 8.lower\",\"size\":0}},\"Custom Field 9\":{\"terms\":{\"field\":\"filters.Custom Field 9.lower\",\"size\":0}},\"Custom Field 10\":{\"terms\":{\"field\":\"filters.Custom Field 10.lower\",\"size\":0}}},\"sort\":[\"_score\",{\"maxPrice\":{\"order\":\"asc\"}}]}"
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
      'content-type': "application/json",
      'cache-control': "no-cache"
      }

  response = requests.request("GET", url, headers=headers)
  data = json.loads(response.text)
  cars = []
  item = {}
  for i in data['vehicles']:
    if i['condition']=='Used':
        getDataVehicle("https://yongesteeles.leadbox.info/data/" + str(i['id']) + ".json")

def getDataVehicle(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers)
    vehicleData = json.loads(response.text)
    cars = []
    item = {}

    item['stockno'] = vehicleData['stocknumber'].encode('utf8')
    item['vin'] = vehicleData['vin'].encode('utf8')
    item['year'] = vehicleData['year'].encode('utf8')
    item['make'] = vehicleData['make'].encode('utf8')
    item['model'] = vehicleData['model'].encode('utf8')
    item['name'] = vehicleData['year'] + ' ' + vehicleData['make'] + ' ' + vehicleData['model']
    item['body_style'] = vehicleData['bodystyle'].encode('utf8')
    item['transmission'] = vehicleData['transmission'].encode('utf8')
    item['engine'] = vehicleData['engine'].encode('utf8')
    item['drivetrain'] = vehicleData['drivetrain'].encode('utf8')

    if len(vehicleData['categories']) > 5: # Because not every vehicle has a 5th category
        item['fuel'] = vehicleData['categories'][5]['features'][0]

    item['price'] = vehicleData['saleprice']
    item['mileage'] = vehicleData['mileage']
    item['horsepower'] = ''
    item['eff_highway'] = vehicleData['fueleconomyhwy']
    item['eff_city'] = vehicleData['fueleconomycity']
    item['description'] = vehicleData['description'].encode('utf8')
    item['trim'] = vehicleData['trim'].encode('utf8')
    item['doors'] = vehicleData['doors']
    item['ex_color'] = vehicleData['exteriorcolor']
    item['in_color'] = vehicleData['interiorcolor']
    item['proof'] = vehicleData['carprooflink']
    item['cert'] = vehicleData['certified']
    item['source_url'] = 'https://yongesteelesfordlincoln.com/view/' + str(vehicleData['id'])

    if len(vehicleData['pictures']) > 0:
        item['main_img'] = "https:" + vehicleData['pictures'][0]
        item['thumb_main_img'] = "https:" + vehicleData['pictures'][0]
        imgsList = ['https:' + i for i in vehicleData['pictures']]
        imgString = ''
        for s in imgsList:
            imgString = imgString + s + "\n"

        item['imgs'] = imgString
        item['thumb_imgs'] = imgString

    else:
        item['main_img'] = "http://v3inventory.edealer.ca/images/new_images_added.png"
        item['thumb_main_img'] = "http://v3inventory.edealer.ca/images/new_images_added.png"
        item['imgs'] = "http://v3inventory.edealer.ca/images/new_images_added.png"
        item['thumb_imgs'] = "http://v3inventory.edealer.ca/images/new_images_added.png"


    writer.writerow([item.get(header) for header in csvHeaders])



if __name__ == '__main__':
  url = "https://yongesteelesfordlincoln.com/data/inventory.json"
  writer = csv.writer(open(csvFileName, 'wb'))
  writer.writerow(csvHeaders)
  getDataMain(url)
