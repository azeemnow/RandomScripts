#Change output encoding:
# -*- coding: utf-8 -*-

import sys
import codecs #"provides access to the internal Python codec registry which manages the codec and error handling lookup process"
sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

import urllib2 #"defines functions and classes which help in opening URLs"
import json #"JavaScript Object Notation"

locu_api = 'ce35372f39cd107c83674ccb3e77c03b13e2a691'

def locu_search(query): #seach by city name function
    api_key = locu_api
    url = 'https://api.locu.com/v1_0/venue/search/?api_key=' + api_key
    locality = query.replace(' ', '%20')
    final_url = url + '&locality=' + locality + "&category=restaurant"
    jason_obj = urllib2.urlopen(final_url) #opens the final version of the URL combined above in final_url variable
    data = json.load(jason_obj) #stores the data obtained while opening the URL above
    for item in data['objects']: #iterates through items located inside the locu "objects" list
        print item['name'], item['phone'], item['street_address'], item['website_url'] #find the specified key & prints associated value

def region_search(query): #search by state function
    api_key = locu_api
    url = 'https://api.locu.com/v1_0/venue/search/?api_key=' + api_key
    region = query.replace(' ', '%20')
    final_url = url + '&region=' + region + "&category=restaurant"
    jason_obj = urllib2.urlopen(final_url)
    data = json.load(jason_obj)
    for item in data['objects']:
        print item['name'], item['phone'], item['street_address'], item['website_url']

def zip_search(query): #search by zip function
    api_key = locu_api
    url = 'https://api.locu.com/v1_0/venue/search/?api_key=' + api_key
    zip = query.replace(' ', '%20')
    final_url = url + '&zip=' + zip + "&category=restaurant"
    jason_obj = urllib2.urlopen(final_url)
    data = json.load(jason_obj)
    for item in data['objects']:
        print item['name'], item['phone'], item['street_address'], item['website_url']

#below loop prompts user to make a selection from 4 choices
#runs user selection against the appropriate query function & print result

ans=True
while ans:
    print ("""
    1.Search by City
    2.Search by Region (State Abbreviation)
    3.Search by Zip
    4.Exit/Quit
    """)
    ans=raw_input("What would you like to do? ")
    if ans=="1":
      locality = raw_input("\nEnter City ")
      print locu_search(locality)
    elif ans=="2":
        region = raw_input("\n Search by State ")
        print region_search(region)
    elif ans=="3":
        zip = raw_input("\n Search by Zip ")
        print zip_search(zip)
    elif ans=="4":
        print (" Goodbye!")
        break

#@azeemnow
#ref:(ref: http://stackoverflow.com/questions/14630288/unicodeencodeerror-charmap-codec-cant-encode-character-maps-to-undefined)