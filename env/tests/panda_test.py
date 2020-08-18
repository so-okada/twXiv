#!/usr/bin/env python3

import threading
import time
import pandas as pd

def pd_write_test(interval):
    log_text = [[1,2,3,4]]
    df = pd.DataFrame(
        log_text,
        columns=['utc', 'total', 'username', 'twitter_id'])
    df.to_csv('test_f.csv', mode='a',  index=None)
    time.sleep(interval)
    print('ended')

