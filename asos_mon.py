from httplib2 import Http
import json
import re
import time


http = Http()
headers = {}
#headers['Accept'] = 'text/html, application/xhtml+xml, */*'
#headers['Accept-Language'] = 'en-us'
#headers['User-Agent'] = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)'
#headers['Accept-Encoding'] = 'gzip, deflate'
#headers['Host'] = 'www.asos.com'
#headers['Cache-Control'] = 'no-cache'

#url = "http://www.asos.com/Men/A-To-Z-Of-Brands/Superdry/Cat/pgecategory.aspx?cid=1623"
#resp, content = http.request(url, "GET", headers = headers)
 
#print resp['set-cookie']

#headers['Cookie'] = resp['set-cookie']
headers['x-requested-with'] = 'XMLHttpRequest'
headers['Accept-Language'] = 'en-us'
headers['Referer'] = 'http://www.asos.com/Men/A-To-Z-Of-Brands/Superdry/Cat/pgecategory.aspx?cid=1623#parentID=-1&pge=0&pgeSize=-1&sort=-1'
headers['Accept'] = 'application/json, text/javascript, */*'
headers['Content-Type'] = 'application/json; charset=utf-8, application/json; charset=utf-8'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Host'] = 'www.asos.com'
headers['Content-Length'] = '142'
headers['Proxy-Connection'] = 'Keep-Alive'
headers['Pragma'] = 'no-cache'
headers['Cookie'] = 'ASP.NET_SessionId=4ipfi2qk1zljydi3hz21c555; asosV=v=; asos=countryid=1&topcatidHitCount=42&topcatid=1001&customerguid=7586fc6eb7ac4069a20c293ce8394402; AsosExecutionEngine=ExemptionTimeout=02/18/2011 06:58; WT_FPC=id=122.116.34.19-3950666976.30026419:lv=1297982309611:ss=1297979564756; asosRITracking=1124909=cid,1623,20110217&1074663=cid,1623,20110217&1289731=cid,1623,20110217&1237347=cid,1623,20110217&1233408=cid,1623,20110217; asosbasket=basketitemcount=0&basketitemtotalretailprice=0; stop_mobi=yes; SSLB=0; __utmc=111878548; __utma=111878548.1622122222.1297922211.1298010432.1298010560.16; __utmz=111878548.1297922211.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=111878548.3.10.1298010560'

url = "http://www.asos.com/services/srvWebCategory.asmx/GetWebCategories"
body = "{'cid':'1623', 'strQuery':\"\", 'strValues':'undefined', 'currentPage':'0', 'pageSize':'-1','pageSort':'-1','countryId':'1','maxResultCount':''}"
#print body
resp, content = http.request(url, "POST", headers = headers, body = body)

if( resp['status'] != '200' ):
  print "abc"
  exit()
else:
  pass
#print content

#
# output
#

def dump(f, item, http, headers):
  price = float(item[u'price'].replace(u'\xa3',''))
  orgPrice = float(item[u'origRP'].replace(u'\xa3',''))
  output = "%s %d %d" % (item[u'desc'], price, orgPrice)
  print " %s %d%%" % (output, int(price / orgPrice*100))   
  #print item
  
  navUrl = 'http://www.asos.com/' + item[u'NavigateURL']
  headers['Content-Length'] = ''
  
  outOfStock = False
  availableSizes = ""
  resp, content = http.request( navUrl, "GET", headers = headers )
  if( resp['status'] == '200' ):
    
    for line in content.splitlines():
      if( line.find('arrSzeCol_ctl00_ContentMainPage_ctlSeparateProduct') == -1 ):
        continue
      
      if( line.find('Out Of Stock') != -1 ):
        outOfStock = True
        break
        
      if( line.find('new Array(') != -1 ):
        #print line
        m = re.search('new Array\((.*)\)', line)
        args = m.group(1).split(',')
        #print args
        if(args[3] == "\"True\""):
          availableSizes += args[1] + ":"
          
  if(outOfStock):
    return
  
  if( availableSizes.find('S') == -1 ):
    return
    
  print availableSizes
  f.write("<span>%s %d %d %s</span><br /><a href=\"http://www.asos.com/%s\"><img src=\"%s\" /></a><br />" % (item[u'desc'], price, orgPrice, availableSizes, item[u'NavigateURL'], item[u'image']))        
        

count = 0;
jsonContent = json.loads(content)

f = open("sales.html", "w")
f.write("<html><head></head><body>")
f.write("<h1>last update: <span>%s</span></h1>" % (time.strftime("%Y/%m/%d %H:%M:%S" , time.localtime())))



for item in jsonContent[u'd'][u'items']:
  
  
  #if(item[u'desc'].find('Shirt') == -1):
  #	continue
  
  if(item[u'desc'].find('Denim') != -1):
    continue
  
  if(item[u'desc'].find('Shoes') != -1):
    continue
    
  if(item[u'desc'].find('Boots') != -1):
    continue
    
  if(item[u'desc'].find('Trainers') != -1):
    continue
  
  price = float(item[u'price'].replace(u'\xa3',''))
  orgPrice = float(item[u'origRP'].replace(u'\xa3',''))
    
  if( item[u'isDiscounted'] ):
    count += 1
    dump(f, item, http, headers)

f.write("</body></html>") 
f.close()