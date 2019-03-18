import time
import requests
from hashlib import sha1
import random
import string
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize


"""
Make a sample call to the Booli API asking for all listings in 'Nacka' in JSON format, 
using 'YOUR_CALLER_ID' and 'YOUR_PRIVATE_KEY' for authentication
"""

private_key = "AhNpKGH4ToJBtmiAdjiSW3SFG1lej3x6UeNQRJn5"
callerId = 'fariz.neubert'

timestamp = str(int(time.time()))
unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
hashstr = sha1((callerId + timestamp + private_key + unique).encode('utf-8')).hexdigest()

headers = {
'Host': 'api.booli.se',
#'Accept': 'application/vnd.booli-v2+json',
'Vary': 'Accept-Encoding',
'Content-Type': 'application/json',
'Connection': 'keep-alive',
    'User - Agent': 'Mozilla / 5.0(Macintosh;'
                    'Intel Mac OS X 10_14_3) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 72.0.3626.96 Safari / 537.36'
}
url = 'https://api.booli.se//sold?areaId=1&offset=35&callerId=' + callerId + '&time=' + timestamp + "&unique=" + unique + '&hash=' + hashstr

response = requests.get(url, headers=headers)

if(response.status_code != 200):
    print("fail")
    print(response.text)
    print(response.status_code)

result = response.json()

sales_data = json_normalize(result['sold'])

