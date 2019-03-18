# import requests
# import numpy as np
# import pandas as pd
# from pandas.io.json import json_normalize
# #import httplib
# import time
# from hashlib import sha1
# import random
# import string
#
# publicKey = 'fariz.neubert'
# callerId = "AhNpKGH4ToJBtmiAdjiSW3SFG1lej3x6UeNQRJn5"
# timestamp = str(int(time.time()))
# unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
# hashstr = sha1((callerId+timestamp+publicKey+unique).encode('utf-8')).hexdigest()
#
# url = "/listings?q=nacka&callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr
#
# session = requests.session()
# req = session.get(url)
#
# if req.status_code != requests.codes.ok:
#     print('fail')
#
# booli_data = req.json()
#
#
# # connection = httplib.HTTPConnection("api.booli.se")
# # connection.request("GET", url)
# # response = connection.getresponse()
# # data = response.read()
# # connection.close()
# #
# # if response.status != 200:
# #     print("fail")
# #
# # result = data
#

import time
import requests
from hashlib import sha1
import random
import string
import json


"""
Make a sample call to the Booli API asking for all listings in 'Nacka' in JSON format, 
using 'YOUR_CALLER_ID' and 'YOUR_PRIVATE_KEY' for authentication
"""


callerId = "AhNpKGH4ToJBtmiAdjiSW3SFG1lej3x6UeNQRJn5"

timestamp = str(int(time.time()))
unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
hashstr = sha1((callerId + timestamp + "fariz.neubert" + unique).encode('utf-8')).hexdigest()

headers = {
'Host': 'api.booli.se',
#'Accept': 'application/vnd.booli-v2+json',
'Vary': 'Accept-Encoding',
'Content-Type': 'application/json',
'Connection': 'keep-alive',
    'User - Agent': 'Mozilla / 5.0(Macintosh;'
                    'Intel Mac OS X 10_14_3) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 72.0.3626.96 Safari / 537.36'
}


#url = "http://api.booli.se/listings?q=nacka&callerId=" + callerId + "&time=" + timestamp + "&unique=" + unique + "&hash=" + hashstr

#url=   https://api.booli.se/listings?q=nacka&limit=3&offset=0&callerId=[callerId]&time=1323793365&unique=3116053465361547264&hash=a053d19fcced8e180df1a40b3fc95b6560eee1af
url = 'https://api.booli.se/listings?q=nacka&limit=3&offset=0&callerId=' + callerId + '&time=' + timestamp + "&unique=" + unique + '&hash=' + hashstr

response = requests.get(url, headers=headers)

if(response.status_code != 200):
    print("fail")
    print(response.text)
    print(response.status_code)
else: result = response.json()

