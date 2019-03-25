import time
from datetime import date
import requests
from hashlib import sha1
import random
import string
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

def get_booli_data():
    private_key = "AhNpKGH4ToJBtmiAdjiSW3SFG1lej3x6UeNQRJn5"
    callerId = 'fariz.neubert'

    timestamp = str(int(time.time()))
    unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
    hashstr = sha1((callerId + timestamp + private_key + unique).encode('utf-8')).hexdigest()

    headers = {
        'Host': 'api.booli.se',
        'Accept': 'application/vnd.booli-v2+json',
        'Vary': 'Accept-Encoding',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'User - Agent': 'Mozilla / 5.0(Macintosh;'
                        'Intel Mac OS X 10_14_3) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 72.0.3626.96 Safari / 537.36'
    }

    BASE_URL = 'https://api.booli.se/'
    limit = 500
    offset = 0
    url = BASE_URL + 'sold?q=innanf%C3%B6r%20tullarna&limit=' + str(limit) + '&offset=' + str(offset) + '&minPublished=20150101&callerId='\
          + callerId + '&time=' + timestamp + "&unique=" + unique + '&hash=' + hashstr

    response = requests.get(url, headers=headers)

    if (response.status_code != 200):
        print("fail")
        print(response.text)
        print(response.status_code)

    result = response.json()
    sales_data = json_normalize(result['sold'])
    total_count = result['totalCount']
    loops = total_count // limit + 1

    for i in range(1, loops):
        timestamp = str(int(time.time()))
        unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
        hashstr = sha1((callerId + timestamp + private_key + unique).encode('utf-8')).hexdigest()
        if i == loops: i = ((loops * limit - total_count) + limit*(i - 1))/ limit
        url = BASE_URL + 'sold?q=innanf%C3%B6r%20tullarna&limit=' + str(limit) + '&offset=' + str(
            offset + limit*i) + '&minPublished=20150101&callerId=' \
              + callerId + '&time=' + timestamp + "&unique=" + unique + '&hash=' + hashstr
        response = requests.get(url, headers=headers)
        try:
            result = response.json()
        except:
            print(response.text)
            pass
        sales_data = sales_data.append(json_normalize(result['sold']), ignore_index = True, sort=False)

    return sales_data

sales = get_booli_data()
sales.to_csv('booli_data ' + str(date.today())+'.csv', index=False, encoding="utf-8")
