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
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry, rate_limited

from variables import *
import twXiv_format as tXf
import twXiv_daily_feed as tXd


def main(switches, logfiles, captions, aliases, pt_mode):
    starting_time = datetime.utcnow().replace(microsecond=0)
    print("**process started at " + str(starting_time) + " (UTC)")

    api_dict = {}
    update_dict = {}
    entries_dict = {}
    caption_dict = {}
    newsubmission_mode = {}

    for cat in switches:
        api_dict[cat] = tweet_api(switches[cat])
        update_dict[cat] = sleep_and_retry(rate_limited(post_updates, a_day)(update))
        newsubmission_mode[cat] = int(switches[cat]["newsubmissions"])
        if cat in captions:
            caption_dict[cat] = captions[cat]
        else:
            caption_dict[cat] = ""

    # retrieval/new submissions
    threads = []
    for i, cat in enumerate(switches):
        th = Thread(
            name=cat,
            target=newentries,
            args=(
                logfiles,
                aliases,
                cat,
                caption_dict[cat],
                api_dict[cat],
                update_dict[cat],
                entries_dict,
                newsubmission_mode[cat],
                pt_mode,
            ),
        )
        threads.append(th)
        ptext = "starting a thread of " + "retrieval/new submissions for " + th.name
        print(ptext)
        th.start()
        if i != len(switches) - 1:
            ptext = "waiting for a next thread of " + "retrieval/new submissions"
            print(ptext)
            time.sleep(main_thread_wait)

    print("joining threads of retrieval/new submissions")
    [th.join() for th in threads]

    if not logfiles:
        ending_time = datetime.utcnow().replace(microsecond=0)

    ending_time = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\n**process ended at "
        + str(ending_time)
        + " (UTC)"
        + "\n**elapsed time from the start: "
        + str(ending_time - starting_time)
    )
    print(ptext)


# tweepy api
def tweet_api(keys):
    return tw.Client(
        consumer_key=keys["consumer_key"],
        consumer_secret=keys["consumer_secret"],
        access_token=keys["access_token"],
        access_token_secret=keys["access_token_secret"],
        wait_on_rate_limit=True,
    )


# tweet under overall limit
@sleep_and_retry
@limits(calls=overall_twitter_limit_call, period=overall_twitter_limit_period)
def update(logfiles, cat, api, total, arxiv_id, text, tw_id_str, pt_method, pt_mode):
    result = 0

    if not pt_mode:
        update_print(cat, arxiv_id, text, tw_id_str, "", pt_method, pt_mode)
        return result

    error_text = (
        "\nthread arXiv category: "
        + cat
        + "\narXiv id: "
        + arxiv_id
        + "\ntext: "
        + text
        + "\ntw_id_str: "
        + tw_id_str
        + "\n"
    )

    if pt_method == "tweet":
        try:
            result = api.create_tweet(text=text)
            update_print(
                cat, arxiv_id, text, tw_id_str, result.data["id"], pt_method, pt_mode
            )
        except Exception:
            time_now = datetime.utcnow().replace(microsecond=0)
            error_text = "\n**error to tweet**" + "\nutc: " + str(time_now) + error_text
            print(error_text)
            traceback.print_exc()
    update_log(logfiles, cat, total, arxiv_id, result, pt_method, pt_mode)
    time.sleep(twitter_sleep)
    return result


# update stdout text format
def update_print(cat, arxiv_id, text, tw_id_str, result_id_str, pt_method, pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = (
        "\nutc: "
        + str(time_now)
        + "\nthread arXiv category: "
        + cat
        + "\narXiv id: "
        + arxiv_id
        + "\nurl: https://x.com/user/status/"
        + tw_id_str
        + "\npost method: "
        + pt_method
        + "\npost mode: "
        + str(pt_mode)
        + "\nurl: https://x.com/user/status/"
        + result_id_str
        + "\ntext: "
        + text
        + "\n"
    )
    print(ptext)


# logging for update
def update_log(logfiles, cat, total, arxiv_id, posting, pt_method, pt_mode):
    if not posting or not pt_mode or not logfiles:
        return None

    time_now = datetime.utcnow().replace(microsecond=0)

    if not arxiv_id and pt_method == "tweet":
        filename = logfiles[cat]["tweet_summary_log"]
        log_text = [[time_now, total, logfiles[cat]["username"], posting.data["id"]]]
        df = pd.DataFrame(log_text, columns=["utc", "total", "username", "twitter_id"])
    else:
        log_text = [[time_now, arxiv_id, logfiles[cat]["username"], posting.data["id"]]]
        df = pd.DataFrame(
            log_text, columns=["utc", "arxiv_id", "username", "twitter_id"]
        )
        filename = logfiles[cat][pt_method + "_log"]

    if not filename:
        return None
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=None, index=None)
    else:
        df.to_csv(filename, mode="w", index=None)


# retrieval of daily entries, and
# calling a sub process for new submissions
def newentries(
    logfiles,
    aliases,
    cat,
    caption,
    api,
    update_limited,
    entries_dict,
    newsubmission_mode,
    pt_mode,
):
    print("getting daily entries for " + cat)
    try:
        entries_dict[cat] = tXd.daily_entries(cat, aliases)
    except Exception:
        entries_dict[cat] = {}
        print("\n**error for retrieval**\nthread arXiv category:" + cat)
        traceback.print_exc()
        if not check_log_dates(cat, "tweet_log", logfiles) and not check_log_dates(
            cat, "tweet_summary_log", logfiles
        ):
            # daily entries retrieval failed and
            # no tweets for today have been made.
            print("check_log_dates returns False for " + cat)
            time_now = datetime.utcnow().replace(microsecond=0)
            ptext = intro(time_now, 0, cat, caption)
            update_limited(logfiles, cat, api, "0", "", ptext, "", "tweet", pt_mode)

    # new submissions
    if newsubmission_mode:
        print("new submissions for " + cat)
        if entries_dict[cat]:
            if len(entries_dict[cat].newsubmissions) < post_updates:
                half = 0
            else:
                half = 1

            newsub_entries = tXf.format(entries_dict[cat].newsubmissions, half)
            if not check_log_dates(cat, "tweet_log", logfiles) and not check_log_dates(
                cat, "tweet_summary_log", logfiles
            ):
                newsubmissions(
                    logfiles, cat, caption, api, update_limited, newsub_entries, pt_mode
                )
            else:
                print(cat + " already tweeted for today")


# an introductory text of each category
# an example: [2020-08-01 (UTC),  4 new articles found for mathCV]
def intro(given_time, num, cat, caption):
    ptext = "[" + given_time.strftime("%Y-%m-%d %a") + " (UTC), "
    # On the variable num, arXiv_feed_parser gives new
    # submissions whose primary subjects are the given category.
    if num == 0:
        ptext = ptext + "no new articles found for "
    elif num == 1:
        ptext = ptext + str(num) + " new article found for "
    else:
        ptext = ptext + str(num) + " new articles found for "
    ptext = ptext + re.sub(r"\.", "", cat)

    if caption:
        ptext = ptext + " " + caption

    if num > 2 * (post_updates - 1):
        ptext = (
            ptext
            + ", but only first "
            + str(2 * (post_updates - 1))
            + " articles to tweet."
            + " See https://arxiv.org/list/"
            + cat
            + "/new"
            + " for more."
            + "]"
        )
    else:
        ptext = ptext + "]"
    return ptext


# new submissions by tweets
def newsubmissions(logfiles, cat, caption, api, update_limited, entries, pt_mode):
    time_now = datetime.utcnow().replace(microsecond=0)
    ptext = intro(time_now, len(entries), cat, caption)
    update_limited(
        logfiles, cat, api, str(len(entries)), "", ptext, "", "tweet", pt_mode
    )
    if len(entries) < post_updates:
        half = 0
    else:
        half = 1

    post_counter = 1
    if half == 0:
        for each in entries:
            arxiv_id = each["id"]
            article_text = (
                each["authors"]
                + ": "
                + each["title"]
                + " "
                + each["abs_url"]
                + " "
                + each["pdf_url"]
                + " "
                + each["html_url"]
            )
            update_limited(
                logfiles, cat, api, "", arxiv_id, article_text, "", "tweet", pt_mode
            )
    else:
        for each in entries:
            pre_arxiv_id = each["id"]
            pre_article_text = (
                each["authors"] + ": " + each["title"] + " " + each["abs_url"]
            )
            if int(post_counter % 2) == 1:
                arxiv_id = pre_arxiv_id
                article_text = pre_article_text
            if int(post_counter % 2) == 0:
                arxiv_id = arxiv_id + " AND " + pre_arxiv_id
                article_text = (
                    article_text
                    + "\n\n"
                    + pre_article_text
                    + "\n\n https://en.wikipedia.org/wiki/Mathematics"
                )

            if int(post_counter % 2) == 0:
                update_limited(
                    logfiles, cat, api, "", arxiv_id, article_text, "", "tweet", pt_mode
                )
            if int(post_counter % 2) == 1 and post_counter == len(entries):
                update_limited(
                    logfiles, cat, api, "", arxiv_id, article_text, "", "tweet", pt_mode
                )
            post_counter += 1


# true if this finds a today's tweet.
def check_log_dates(cat, logname, logfiles):
    if not logfiles:
        print("no log files")
        return False

    filename = logfiles[cat][logname]
    if not os.path.exists(filename):
        print("log file does not exists: " + filename)
        return False

    time_now = datetime.utcnow().replace(microsecond=0)
    try:
        df = pd.read_csv(filename, dtype=object)
    except Exception:
        error_text = "\nutc: " + str(time_now) + "\nfilename: " + filename
        error_text = "\n**error for pd.read_csv**" + error_text
        print(error_text)
        traceback.print_exc()
        return False
    for index, row in df.iterrows():
        log_time = datetime.fromisoformat(row["utc"])
        if (
            check_dates(log_time, time_now)
            and row["username"] == logfiles[cat]["username"]
        ):
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
