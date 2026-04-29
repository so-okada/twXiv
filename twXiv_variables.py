# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds, a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_feed_timeout = 60
arxiv_max_trial = 3
arxiv_call_sleep = 15 * 60
main_thread_wait = 40

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
min_len_authors_short = int(min_len_authors / 2) - 10
min_len_title = 150
min_len_title_short = int(min_len_title / 2) - 10

# for 2-paper posts: budget per entry in a 280-char tweet
# 280 total - 2 chars for one "\n\n" separator = 278, divided by 2
max_len_second = int((max_len - 2) / 2)
arxiv_identifier_len_second = 17  # " arXiv:XXXX.YYYY" as plain text (not a URL)
min_len_title_second = 40

# for 3-paper posts: budget per entry in a 280-char tweet
# 280 total - 4 chars for two "\n\n" separators = 276, divided by 3
max_len_third = int((max_len - 4) / 3)
arxiv_identifier_len_third = 17  # " arXiv:XXXX.YYYY" as plain text (not a URL)
min_len_title_third = 30
newsub_spacer = 2
margin = 2

# rate limit for each category
# https://devcommunity.x.com/t/specifics-about-the-new-free-tier-rate-limits/229761/2
a_day = 24 * 60 * 60
post_updates = 16

# limits independent to specific categories
twitter_sleep = 2
overall_twitter_limit_call = 1
overall_twitter_limit_period = 4
