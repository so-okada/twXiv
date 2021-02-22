#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of twXiv for posting to twitter and stdout
# https://github.com/so-okada/twXiv/

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
import twXiv_daily_feed as tXd
import twXiv_semantic as tXs


def main(switches, logfiles, captions, aliases, pt_mode):
    starting_time = datetime.utcnow().replace(microsecond=0)
    print('**process started at ' + str(starting_time) + ' (UTC)')

    api_dict = {}
    update_dict = {}
    entries_dict = {}
    webreplacements_dict = {}
    caption_dict = {}

    newsubmission_mode = {}
    abstract_mode = {}
    crosslist_mode = {}
    quote_replacement_mode = {}
    retweet_replacement_mode = {}

    for cat in switches:
        api_dict[cat] = tweet_api(switches[cat])
        update_dict[cat] = sleep_and_retry(
            rate_limited(post_updates, three_hours)(update))
        newsubmission_mode[cat] = int(switches[cat]['newsubmissions'])
        abstract_mode[cat] = int(switches[cat]['abstracts'])
        crosslist_mode[cat] = int(switches[cat]['crosslists'])
        quote_replacement_mode[cat] = int(
            switches[cat]['quote_replacements'])
        retweet_replacement_mode[cat] = int(
            switches[cat]['retweet_replacements'])
        if cat in captions:
            caption_dict[cat] = captions[cat]
        else:
            caption_dict[cat] = ''

    # retrieval/new submissions/abstracts
    threads = []
    for i, cat in enumerate(switches):
        th = Thread(name=cat,
                    target=newentries,
                    args=(logfiles, aliases, cat, caption_dict[cat],
                          api_dict[cat], update_dict[cat],
                          entries_dict, newsubmission_mode[cat],
                          abstract_mode[cat], pt_mode))
        threads.append(th)
        ptext = \
            'starting a thread of ' +\
            'retrieval/new submissions/abstracts for ' +\
            th.name
        print(ptext)
        th.start()
        if i != len(switches) - 1:
            ptext = 'waiting for a next thread of ' + \
                'retrieval/new submissions/abstracts'
            print(ptext)
            time.sleep(main_thread_wait)

    print('joining threads of retrieval/new submissions/abstracts')
    [th.join() for th in threads]

    if not logfiles:
        ending_time = datetime.utcnow().replace(microsecond=0)
        if crosslist_mode[cat] or crosslist_mode[cat]:
            ptext = \
                'No logfiles found. ' + \
                'twXiv needs logfiles for cross-lists and replacements ' +\
                'by reweets and unretweets.'
            print(ptext)
            ptext = '\n**process ended at ' + str(ending_time) + ' (UTC)' +\
                '\n**elapsed time from the start: ' + \
                str(ending_time - starting_time)
            print(ptext)
            return None

    # cross lists
    crosslist_time = datetime.utcnow().replace(microsecond=0)
    ptext = \
        '\n**cross-list process started at ' + str(crosslist_time) + \
        ' (UTC)' + ' \n**elapsed time from the start: ' +\
        str(crosslist_time - starting_time)
    print(ptext)

    threads = []
    for i, cat in enumerate(switches):
        if entries_dict[cat] and crosslist_mode[cat]:
            crosslist_entries = entries_dict[cat].crosslists
            th = Thread(name=cat,
                        target=crosslists,
                        args=(logfiles, cat, api_dict[cat],
                              update_dict[cat], crosslist_entries,
                              pt_mode))
            threads.append(th)
            print('start a cross-list thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next cross-list thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining cross-list threads')
        [th.join() for th in threads]

    # replacements
    replacement_time = datetime.utcnow().replace(microsecond=0)
    ptext = \
        '\n**replacement process started at ' + \
        str(replacement_time) + ' (UTC)' + \
        '\n**elapsed time from the start: ' + \
        str(replacement_time - starting_time) + \
        '\n**elapsed time from the cross-list start: ' + \
        str(replacement_time - crosslist_time)
    print(ptext)

    print("quote-replacement starts")
    for i, cat in enumerate(switches):
        if entries_dict[cat]:
            replacement_entries = entries_dict[cat].replacements
            # version check: new sub web pages exclude versions > 5.
            webreplacements_dict[cat] = []
            for each in replacement_entries:
                if not each['version'] == '' and int(
                        each['version']) > 5:
                    print('version unknown or >5 for ' + each['id'])
                    # exclude old arXiv identifiers
                elif not re.match('[a-z|A-Z]', each['id']):
                    webreplacements_dict[cat].append(each)

    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and quote_replacement_mode[cat]:
            th = Thread(name=cat,
                        target=quote_replacement,
                        args=(logfiles, cat, api_dict[cat],
                              update_dict[cat],
                              webreplacements_dict[cat], pt_mode))
            threads.append(th)
            print('start a quote-replacement thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next quote-replacement thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining quote-replacement threads')
        [th.join() for th in threads]

    print("retweet-replacement starts")
    threads = []
    for i, cat in enumerate(switches):
        if webreplacements_dict[cat] and retweet_replacement_mode[cat]:
            th = Thread(name=cat,
                        target=retweet_replacement,
                        args=(logfiles, cat, api_dict[cat],
                              update_dict[cat],
                              webreplacements_dict[cat], pt_mode))
            threads.append(th)
            print('start a retweet-replacement thread of ' + th.name)
            th.start()
            if i != len(switches) - 1:
                print('waiting for a next retweet-replacement thread')
                time.sleep(main_thread_wait)

    if threads:
        print('joining retweet-replacement threads')
        [th.join() for th in threads]

    ending_time = datetime.utcnow().replace(microsecond=0)
    ptext = '\n**process ended at ' + str(ending_time) + ' (UTC)' +\
        '\n**elapsed time from the start: ' + \
        str(ending_time - starting_time) + \
        '\n**elapsed time from the cross-list start: ' + \
        str(ending_time - crosslist_time) + \
        '\n**elapsed time from the replacement start: ' + \
        str(ending_time - replacement_time)
    print(ptext)


# tweepy api
def tweet_api(keys):
    ckey = keys['consumer_key']
    csecret = keys['consumer_secret']
    atoken = keys['access_token']
    atoken_secret = keys['access_token_secret']
    auth = tw.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, atoken_secret)

    return tw.API(auth,
                  wait_on_rate_limit_notify=True,
                  wait_on_rate_limit=True,
                  retry_count=3,
                  retry_delay=12)


# tweet/retweet/unretweet/reply/quote with overall limit
@sleep_and_retry
@limits(calls=overall_twitter_limit_call,
        period=overall_twitter_limit_period)
def update(logfiles, cat, api, total, arxiv_id, text, tw_id_str,
           pt_method, pt_mode):
    result = 0

    if not pt_mode:
        update_print(cat, arxiv_id, text, tw_id_str, '', pt_method,
                     pt_mode)
        return result

    error_text = '\nthread arXiv category: ' + cat + \
        '\narXiv id: ' + arxiv_id + \
        '\ntext: ' + text + \
        '\ntw_id_str: ' + tw_id_str + '\n'

    if pt_method == 'tweet':
        try:
            result = api.update_status(text)
            update_print(cat, arxiv_id, text, tw_id_str,
                         result.id_str, pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to tweet**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'retweet':
        try:
            result = api.retweet(tw_id_str)
            update_print(cat, arxiv_id, text, tw_id_str,
                         result.id_str, pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to retweet**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'unretweet':
        try:
            result = api.unretweet(tw_id_str)
            update_print(cat, arxiv_id, text, tw_id_str,
                         result.id_str, pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to unretweet**' + \
                '\nutc: ' + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'reply':
        try:
            result = api.update_status(
                text, in_reply_to_status_id=tw_id_str)
            update_print(cat, arxiv_id, text, tw_id_str,
                         result.id_str, pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to reply**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()
    elif pt_method == 'quote':
        try:
            result = api.update_status(text)
            update_print(cat, arxiv_id, text, tw_id_str,
                         result.id_str, pt_method, pt_mode)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\n**error to quote**' + '\nutc: ' + str(time_now) + \
                error_text
            print(error_text)
            traceback.print_exc()

    update_log(logfiles, cat, total, arxiv_id, result, pt_method,
               pt_mode)
    time.sleep(twitter_sleep)
    return result


# update stdout text format
def update_print(cat, arxiv_id, text, tw_id_str, result_id_str,
                 pt_method, pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = '\nutc: ' + str(time_now) + \
        '\nthread arXiv category: ' + cat +\
        '\narXiv id: ' + arxiv_id + \
        '\nurl: https://twitter.com/user/status/' + tw_id_str +\
        '\npost method: ' + pt_method +\
        '\npost mode: ' + str(pt_mode) +\
        '\nurl: https://twitter.com/user/status/' + result_id_str + \
        '\ntext: ' + text + '\n'
    print(ptext)


# logging for update
def update_log(logfiles, cat, total, arxiv_id, posting, pt_method,
               pt_mode):
    if not posting or not pt_mode or not logfiles:
        return None

    time_now = datetime.utcnow().replace(microsecond=0)

    if not arxiv_id and pt_method == 'tweet':
        filename = logfiles[cat]['tweet_summary_log']
        log_text = [[
            time_now, total, logfiles[cat]['username'], posting.id_str
        ]]
        df = pd.DataFrame(
            log_text,
            columns=['utc', 'total', 'username', 'twitter_id'])
    else:
        log_text = [[
            time_now, arxiv_id, logfiles[cat]['username'],
            posting.id_str
        ]]
        df = pd.DataFrame(
            log_text,
            columns=['utc', 'arxiv_id', 'username', 'twitter_id'])
        filename = logfiles[cat][pt_method + '_log']

    if not filename:
        return None
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None, index=None)
    else:
        df.to_csv(filename, mode='w', index=None)


# retrieval of daily entries, and
# calling a sub process for new submissions and abstracts
def newentries(logfiles, aliases, cat, caption, api, update_limited,
               entries_dict, newsubmission_mode, abstract_mode,
               pt_mode):
    print("getting daily entries for " + cat)
    try:
        entries_dict[cat] = tXd.daily_entries(cat, aliases)
    except Exception:
        entries_dict[cat] = {}
        print("\n**error for retrieval**\nthread arXiv category:" +
              cat)
        traceback.print_exc()
        if not check_log_dates(cat, 'tweet_log', logfiles) and \
           not check_log_dates(cat, 'tweet_summary_log', logfiles):
            # daily entries retrieval failed and
            # no tweets for today have been made.
            print("check_log_dates returns False for " + cat)
            time_now = datetime.utcnow().replace(microsecond=0)
            ptext = intro(time_now, 0, cat, caption)
            update_limited(logfiles, cat, api, '0', '', ptext, '',
                           'tweet', pt_mode)

    # new submissions and abstracts
    if newsubmission_mode:
        print("new submissions for " + cat)
        if entries_dict[cat]:
            newsub_entries = tXf.format(
                entries_dict[cat].newsubmissions)
            if not check_log_dates(cat, 'tweet_log', logfiles) and \
               not check_log_dates(cat, 'tweet_summary_log', logfiles):
                newsubmissions(logfiles, cat, caption, api,
                               update_limited, newsub_entries,
                               abstract_mode, pt_mode)
            else:
                print(cat + ' already tweeted for today')


# an introductory text of each category
# an example: [2020-08-01 (UTC),  4 new articles found for mathCV]
def intro(given_time, num, cat, caption):
    ptext = '[' + \
        given_time.strftime('%Y-%m-%d %a') + ' (UTC), '
    # On the variable num, arXiv_feed_parser gives new
    # submissions whose primary subjects are the given category.
    if num == 0:
        ptext = ptext + \
            "no new articles found for "
    elif num == 1:
        ptext = ptext + str(num) + \
            " new article found for "
    else:
        ptext = ptext + str(num) + \
            " new articles found for "
    if caption:
        ptext = ptext + re.sub(r'\.', '', cat) + " " + caption + "]"
    else:
        ptext = ptext + re.sub(r'\.', '', cat) + "]"
    return ptext


# new submissions by tweets and abstracts by replies
def newsubmissions(logfiles, cat, caption, api, update_limited,
                   entries, abstract_mode, pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = intro(time_now, len(entries), cat, caption)
    update_limited(logfiles, cat, api, str(len(entries)), '', ptext,
                   '', 'tweet', pt_mode)

    for each in entries:
        arxiv_id = each['id']
        article_text = \
            each['authors'] + ": " + \
            each['title'] + " " + \
            each['abs_url'] + " " + \
            each['pdf_url']
        posting = update_limited(logfiles, cat, api, '', arxiv_id,
                                 article_text, '', 'tweet', pt_mode)

        if abstract_mode and posting:
            sep_abst = each['separated_abstract']
            for i, partial_abst in enumerate(sep_abst):
                if i == 0:
                    abst_posting = update_limited(
                        logfiles, cat, api, '', arxiv_id,
                        partial_abst, posting.id_str, 'reply',
                        pt_mode)
                else:
                    abst_posting = update_limited(
                        logfiles, cat, api, '', arxiv_id,
                        partial_abst, abst_posting.id_str, 'reply',
                        pt_mode)
                if abst_posting == 0:
                    break


# crosslists by retweets
def crosslists(logfiles, cat, api, update_limited, entries, pt_mode):
    # if-clause to avoid duplication errors
    # when twXiv runs twice with cross-lists in a day.

    retweet_filename = logfiles[cat]['retweet_log']
    time_now = datetime.utcnow().replace(microsecond=0)
    error_text = '\nutc: ' + str(
        time_now) + '\nretweet_filename: ' + retweet_filename
    if os.path.exists(retweet_filename):
        try:
            dretweet_f = pd.read_csv(retweet_filename, dtype=object)
        except Exception:
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False
        for retweet_index, retweet_row in dretweet_f.iterrows():
            try:
                log_time = retweet_row['utc']
            except Exception:
                error_text = "\n**error for row['utc']**" + error_text
                print(error_text)
                traceback.print_exc()
            log_time = datetime.fromisoformat(log_time)
            if check_dates(time_now, log_time):
                ptext = 'already retweeted today for cross-lists: ' + cat
                print(ptext)
                return None

    for each in entries:
        arxiv_id = each['id']
        subject = each['primary_subject']
        print(cat, ' ', arxiv_id, ' ', subject)

        if subject == cat:
            # This case is not listed in new submission web pages,
            # but was in rss feeds (2020-06-14).
            ptext = 'skip: cross-list of an article in its own category \n'
            print(ptext)
            continue
        if subject not in logfiles.keys():
            print('not in logfiles: ' + subject)
            continue

        tweet_filename = logfiles[subject]['tweet_log']
        # skip without tweet_log
        if not os.path.exists(tweet_filename):
            print('no tweet log file for ' + subject)
            continue

        # open tweet_log file
        try:
            tweet_df = pd.read_csv(tweet_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\nutc: ' + str(
                time_now) + '\ntweet_filename: ' + tweet_filename
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False

        time_now = datetime.utcnow().replace(microsecond=0)
        for tweet_index, tweet_row in tweet_df.iterrows():
            if arxiv_id == tweet_row['arxiv_id']:
                twitter_id = tweet_row['twitter_id']
                tweet_time = datetime.fromisoformat(tweet_row['utc'])
                # if-clause to avoid double retweets
                if not check_dates(time_now, tweet_time):
                    update_limited(logfiles, cat, api, '', arxiv_id,
                                   '', twitter_id, 'unretweet',
                                   pt_mode)
                update_limited(logfiles, cat, api, '', arxiv_id, '',
                               twitter_id, 'retweet', pt_mode)


# replacements by quotes and retweets
def quote_replacement(logfiles, cat, api, update_limited, entries,
                      pt_mode):

    tweet_filename = logfiles[cat]['tweet_log']
    # skip without tweet_log
    if not os.path.exists(tweet_filename):
        print('no tweet log file for ' + cat)
        return None

    # open tweet_log file
    try:
        tweet_df = pd.read_csv(tweet_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = '\nutc: ' + str(
            time_now) + '\ntweet_filename: ' + tweet_filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False

    quote_filename = logfiles[cat]['quote_log']
    # skip without quote_log with posting mode
    if not os.path.exists(tweet_filename) and pt_mode:
        print('posting mode without quote log file for ' + cat)
        return None

    # open quote_log file
    try:
        quote_df = pd.read_csv(quote_filename, dtype=object)
    except Exception:
        time_now = datetime.utcnow().replace(microsecond=0)
        error_text = '\nutc: ' + str(
            time_now) + '\nquote_filename: ' + quote_filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False

    # if-clause to avoid duplication errors
    time_now = datetime.utcnow().replace(microsecond=0)
    if pt_mode and \
       any(check_dates(time_now, datetime.fromisoformat(t))
           for t in quote_df.utc.values):
        print('already made quote-replacements today for ' + cat)
        return None

    entries_to_quote = []
    for each in entries:
        arxiv_id = each['id']
        if each['primary_subject'] == cat and \
           not any(arxiv_id == tweet_row['arxiv_id']
                for tweet_index, tweet_row in quote_df.iterrows()):
            entries_to_quote.append(each)

    for each in entries_to_quote:
        arxiv_id = each['id']
        username = logfiles[cat]['username']
        ptext = 'This https://arxiv.org/abs/' + arxiv_id + \
            ' has been replaced. ' + \
            tools(arxiv_id)

        for tweet_index, tweet_row in tweet_df.iterrows():
            if arxiv_id == tweet_row['arxiv_id']:
                twitter_id = tweet_row['twitter_id']
                ptext = ptext + ' https://twitter.com/' + username + \
                    '/status/' + twitter_id
                update_limited(logfiles, cat, api, '', arxiv_id,
                               ptext, twitter_id, 'quote', pt_mode)


def retweet_replacement(logfiles, cat, api, update_limited, entries,
                        pt_mode):
    for each in entries:
        arxiv_id = each['id']
        subject = each['primary_subject']

        if subject not in logfiles.keys():
            print('No quote log for ' + subject)
            continue
        quote_filename = logfiles[subject]['quote_log']

        # skip without quote_log
        if not os.path.exists(quote_filename):
            print('no quote log file for ' + subject)
            continue

        # open quote_log
        try:
            quote_df = pd.read_csv(quote_filename, dtype=object)
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = '\nutc: ' + str(
                time_now) + '\nquote_filename: ' + quote_filename
            error_text = '\n**error for pd.read_csv**' + error_text
            print(error_text)
            traceback.print_exc()
            return False

        # unretweet and retweet
        for tweet_index, tweet_row in quote_df.iterrows():
            # check if arxiv_id is in quote_log.
            if arxiv_id == tweet_row['arxiv_id']:
                log_time = tweet_row['utc']
                log_time = datetime.fromisoformat(log_time)
                time_now = datetime.utcnow().replace(microsecond=0)
                if cat != subject or not check_dates(
                        time_now, log_time):
                    twitter_id = tweet_row['twitter_id']
                    update_limited(logfiles, cat, api, '', arxiv_id,
                                   '', twitter_id, 'unretweet',
                                   pt_mode)
                    update_limited(logfiles, cat, api, '', arxiv_id,
                                   '', twitter_id, 'retweet', pt_mode)


# true if this finds a today's tweet.
def check_log_dates(cat, logname, logfiles):
    if not logfiles:
        print('no log files')
        return False

    filename = logfiles[cat][logname]
    if not os.path.exists(filename):
        print('log file does not exists: ' + filename)
        return False

    time_now = datetime.utcnow().replace(microsecond=0)
    try:
        df = pd.read_csv(filename, dtype=object)
    except Exception:
        error_text = '\nutc: ' + str(
            time_now) + '\nfilename: ' + filename
        error_text = '\n**error for pd.read_csv**' + error_text
        print(error_text)
        traceback.print_exc()
        return False
    for index, row in df.iterrows():
        log_time = datetime.fromisoformat(row['utc'])
        if check_dates(log_time, time_now) and \
           row['username'] == logfiles[cat]['username']:
            return True
    return False


# true if dates of input times are the same during weekdays
# extended match during weekends
def check_dates(time1, time2):
    time1w = time1.weekday()
    time2w = time2.weekday()
    if time1w >= 5:
        time1 = time1 - timedelta(time1w - 4)
    if time2w >= 5:
        time2 = time2 - timedelta(time2w - 4)
    if time1.date() == time2.date():
        return True
    else:
        return False


def tools(arxiv_id):
    google_url = 'https://scholar.google.com/scholar?q=arXiv%3A' +\
        arxiv_id
    semantic_url = 'https://www.semanticscholar.org/paper/'
    ctdp_url = 'https://www.connectedpapers.com/main/'
    paperid = ''

    try:
        paperid = tXs.paperid('arXiv:' + arxiv_id)
    except Exception:
        error_text = '\narXiv_id: ' + arxiv_id
        error_text = '\n**error for sch_paperid**' + error_text
        print(error_text)

    if paperid:
        urls = google_url + ' ' + \
            semantic_url + paperid + ' ' + \
            ctdp_url + paperid
        return 'Links: ' + urls
    else:
        return 'Link: ' + google_url
