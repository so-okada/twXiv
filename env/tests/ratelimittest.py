#!/usr/bin/env python3

import requests
import re
import json
import time
import traceback
from threading import Thread
import tweepy as tw
import pandas as pd
from ratelimit import limits,sleep_and_retry,rate_limited
from datetime import datetime,date,timedelta



@sleep_and_retry
@limits(calls=1, period=0.5)
def call_test(i):
  tdate=datetime.utcnow()
  print(i,' ',str(tdate))

def hfunction(i,f):
  for index in range(5):
    f(i)
    
def test(num):
  function_dict={}
  for i in range(num):
    function_dict[i]=\
      sleep_and_retry(rate_limited(1, 5)(call_test))
  print(function_dict)

  for i in range(num):
        th= Thread(name=str(i),target=hfunction,
                   args=(i,function_dict[i]))
#        print(i)
        th.start()
