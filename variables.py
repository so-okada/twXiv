# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds, a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_max_trial = 5
arxiv_call_sleep = 20 * 60
main_thread_wait = 60

# max tweet length is 280
# twitter url length is 23
# 2020-06-14
max_len = 280
max_len_short = int(max_len / 2) - 24
url_len = 23

# tweets for new submissions:
url_margin = 2
urls_len = (url_len + url_margin) * 3
urls_len_short = urls_len
min_len_authors = 70
min_len_authors_short = int(min_len_authors / 2)
min_len_title = 150
min_len_title_short = int(min_len_title / 2)
newsub_spacer = 2
margin = 2

# rate limit for each category
# https://developer.x.com/en/products/twitter-api
a_day = 24 * 60 * 60
post_updates = 9

# limits independent to specific categories
twitter_sleep = 2
overall_twitter_limit_call = 1
overall_twitter_limit_period = 4
