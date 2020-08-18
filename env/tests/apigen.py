import re
import os
import time
import traceback
import tweepy as tw
import pandas as pd
from threading import Thread
from datetime import datetime, date, timedelta
from ratelimit import limits, sleep_and_retry, rate_limited

from variables import *
import twXiv_format as tXf
# twXiv uses arXiv rss feeds by default.
# import twXiv_daily_newhtml as tXd
import twXiv_daily_feed as tXd


def api_check(switches):
    starting_time = datetime.utcnow().replace(microsecond=0)
    print('*process started at ' + str(starting_time) + ' (UTC)')

    api_dict = {}
    newsubmission_mode = {}
    abstract_mode = {}
    crosslist_mode = {}
    replacement_mode = {}

    for cat in switches:
        api_dict[cat] = tXp.tweet_api(switches[cat])
        newsubmission_mode[cat] = int(switches[cat]['newsubmissions'])
        abstract_mode[cat] = int(switches[cat]['abstracts'])
        crosslist_mode[cat] = int(switches[cat]['crosslists'])
        replacement_mode[cat] = int(switches[cat]['replacements'])
        print(cat,
              api_dict[cat],
              newsubmission_mode[cat],
              abstract_mode[cat],
              crosslist_mode[cat],
              replacement_mode[cat])
    return api_dict
