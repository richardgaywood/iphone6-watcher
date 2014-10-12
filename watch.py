#!/usr/bin/python

# Python script to watch for iPhone 6 availability.

# Based on https://gist.github.com/andyberry88/6728fa0c631b1ec5e84f by Andy Berry
# and https://gist.github.com/nikf/e78c50c121d858522de5 by Nik Flectcher

from __future__ import division
import json, urllib2, time, smtplib, sys, datetime, time
from pprint import pprint
from email.mime.text import MIMEText

#### USER CONFIGURATON STARTS HERE ####

# See http://www.everymac.com/systems/apple/iphone/specs/apple-iphone-6-a1586-4.7-inch-sprint-global-international-specs.html
# and http://www.everymac.com/systems/apple/iphone/specs/apple-iphone-6-plus-a1524-5.5-inch-sprint-global-international-specs.html
# MG4F2B/A = iPhone 6, 64 GB, "Space Black"
wantedModel = 'MG4F2B/A'
# Use this value for testing
#wantedModel = 'MGA92B/A'

# See http://www.ifoapplestore.com/store-number-list/
wantedStores = ['R245', 'R092', 'R227', 'R226', 'R163'];

# Email settings; any gmail account should work in here. Obviously
# putting your password in here is a filthy hack that I cannot condone.
send_email_enabled = False # Change this to True if you want to send an email
smtp_server = 'smtp.gmail.com'
smtp_from_address = 'USERNAME@gmail.com'
smtp_password = 'PASSWORD'
smtp_to_address = 'someone@somewhere.com'

#### USER CONFIGURATON ENDS HERE ####

storesUrl = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/stores.json'
stockUrl = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability.json'

# Used to generate a CSV with stats
f=open("out.csv","a", 0)

storeNames = dict()

def get_store_names():
  storeNameData = json.load(urllib2.urlopen(storesUrl))
  if 'stores' in storeNameData:
    for storeNameDatum in storeNameData['stores']:
      storeNames[storeNameDatum['storeNumber']] = storeNameDatum['storeName']
    return True
  else:
    return False

def get_stock():
  data = json.load(urllib2.urlopen(stockUrl))
  #pprint(data)
  count_stock(data)

  report = ""
  for wantedStore in wantedStores:
    if (data[wantedStore][wantedModel]):
      report += "<p>Got model " + wantedModel + " in store " + storeNames[wantedStore] +"</p>"
  return report

def count_stock(data):
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

  count = 0
  total = 0

  for store in data:
    if type(data[store]).__name__ == 'dict':
      for model in data[store]:
        total += 1
        if data[store][model]:
          count += 1
	
  if total>0: # Guard against div-by-zero error if service is down.
    percentage = count/total*100
  else:
    percentage = 0

  print "At %s, there are %d combinations of SKU and store marked as in stock (%.0f%%)." % (st, count, percentage)
  f.write("%s,%d,%.0f%%\n" % (st, count, percentage))

def send_email(report):
  if send_email_enabled == False:
    return

  session = smtplib.SMTP(smtp_server, 587)
  session.ehlo()
  session.starttls()
  session.login(smtp_from_address, smtp_password)

  headers = "\r\n".join(["from: " + smtp_from_address,
                       "subject: iPhones are available!",
                       "to: " + smtp_to_address,
                       "mime-version: 1.0",
                       "content-type: text/html"])

  content = headers + "\r\n\r\n" + report
  content += '<p>Go here for more: <a href="https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability</p>'
  session.sendmail("richardgaywood@gmail.com", "rich@fscked.co.uk", content)


email_count = 0
while True: # Infinite loop.
  try:
    if get_store_names(): # Returns false when service is down.
      report = get_stock()
      if len(report) > 0:
        if (email_count <= 0): # Throttle email sending to be less spammy.
          send_email(report)
          email_count = 20
        print report
      email_count -= 1
    else:
      ts = time.time()
      st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
      print "At %s, service is down." % st
  except:
    print "Unexpected error:", sys.exc_info()[0]
  time.sleep(30)

