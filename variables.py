# max tweet length is 280
# twitter url length is 23
# 2020-06-14

max_len = 280
url_len = 23
url_margin = 2

# tweets for new submissions:
# min_len_authors+2+min_len_title+1+urls_len+margin
# =90+128+50+3+9
# =280
# =max_len

urls_len = (url_len + url_margin) * 2
min_len_authors = 90
min_len_title = 128
newsub_spacer = 3
margin = 9

# abstract tag for a counter and url
abst_tag = 11 + (url_len + url_margin) + 1

# arXiv API rate limits  2020-06-16
# no more than 1 request every 3 seconds, a single connection at a time.
# https://arxiv.org/help/api/tou
arxiv_call_limit = 1
arxiv_call_period = 5

arxiv_max_trial = 6
arxiv_call_sleep = 20 * 60

main_thread_wait = 60


# 300 tweets/retweets/unretweets/replies (combined)
# per user account and 3 hours
# https://developer.twitter.com/en/docs/basics/rate-limits 2020-07-02
# https://stackoverflow.com/questions/59797923/how-to-find-post-friendships-create-limit-with-tweepy-in-python-3
# twXiv uses ratelimit library, assuming that different arXiv
# categories use different user accounts.
three_hours = 3 * 60 * 60
post_updates = 260
twitter_sleep = 9

# overall posting limit independent to specific categories
overall_twitter_limit_call = 1
overall_twitter_limit_period = 5

# semanticscholar API rate limits  2020-12-30
# The API is freely available, but enforces a rate limit and will respond
# with HTTP status 429 'Too Many Requests' if the limit is exceeded
# (100 requests per 5 minute window per IP address).
# https://api.semanticscholar.org/
sch_call_limit = 90
sch_call_period = 5 * 60

sch_max_trial = 6
sch_call_sleep = 3
