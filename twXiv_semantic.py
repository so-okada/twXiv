#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of twXiv
# https://github.com/so-okada/twXiv/

import re
import time
from ratelimit import limits, sleep_and_retry, rate_limited
from variables import *

from semanticscholar import SemanticScholar
sch = SemanticScholar(timeout=5)

@sleep_and_retry
@limits(calls=sch_call_limit, period=sch_call_period)
def paperid(arxiv_id):
    trial_num = 0
    while trial_num < sch_max_trial:
        paper = sch.get_paper(arxiv_id)
        if paper == {}:
            print(str(trial_num + 1) + 'th sch parse error for ' + arxiv_id)
        else:
            return re.sub('https://www.semanticscholar.org/paper/', '',
                          paper['url'])
        trial_num += 1
        if trial_num < sch_max_trial:
            print('sleep and retry for ' + arxiv_id)
            time.sleep(sch_call_sleep)
        else:
            raise Exception('fatal parse error for ' + arxiv_id)
