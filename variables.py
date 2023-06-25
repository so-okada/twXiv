# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds, a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_max_trial = 5
arxiv_call_sleep = 20 * 60
main_thread_wait = 60

# semanticscholar API rate limits  2020-12-30
# 100 requests per 5 minutes. 
# https://api.semanticscholar.org/
sch_call_period = 5 * 60
sch_call_limit = 90
sch_max_trial = 2
sch_call_sleep = 5

# max tweet length is 280
# twitter url length is 23
# 2020-06-14
max_len = 280
url_len = 23

# tweets for new submissions:
# min_len_authors+min_len_title+urls_len=268
url_margin = 2
urls_len = (url_len + url_margin) * 2
min_len_authors = 90
min_len_title = 128
newsub_spacer = 3
margin = 5

# abstract tag for a counter and url
abst_tag = 11 + (url_len + url_margin) + 1

# rate limit for each category
# https://developer.twitter.com/en/products/twitter-api
a_day = 24 * 60 * 60
post_updates = 50

# limits independent to specific categories
twitter_sleep = 9
overall_twitter_limit_call = 1
overall_twitter_limit_period = 5
