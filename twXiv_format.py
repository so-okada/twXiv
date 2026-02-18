#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of twXiv for formatting arXiv metadata
# https://github.com/so-okada/twXiv/

import re
from twitter_text import parse_tweet
from nameparser import HumanName
from twXiv_variables import *


# format all new submissions
def format(entries, half):
    return [format_each(one, half) for one in entries]


# format each new submission
def format_each(orig_entry, half):
    if half == 1:
        global max_len
        global urls_len
        global min_len_authors
        global min_len_title
        max_len = max_len_short
        urls_len = urls_len_short
        min_len_authors = min_len_authors_short
        min_len_title = min_len_title_short

    fixed_length = urls_len + newsub_spacer + margin
    entry = orig_entry.copy()
    orig_title = entry["title"]

    authors_title = entry["authors"] + entry["title"]
    current_len = parse_tweet(authors_title).weightedLength + fixed_length

    # first,  a title
    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = parse_tweet(entry["title"]).weightedLength
        lim = max(min_len_title, current_len_title - difference)
        entry["title"] = simple(entry["title"], lim)

    authors_title = entry["authors"] + entry["title"]
    current_len = parse_tweet(authors_title).weightedLength + fixed_length

    # second, authors
    if current_len > max_len:
        difference = current_len - max_len
        current_len_authors = parse_tweet(entry["authors"]).weightedLength
        lim = max(min_len_authors, current_len_authors - difference)
        entry["authors"] = authors(entry["authors"], lim)

    # third,  a longer title if the length of authors' names becomes shorter
    entry["title"] = orig_title
    authors_title = entry["authors"] + entry["title"]
    current_len = parse_tweet(authors_title).weightedLength + fixed_length

    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = parse_tweet(entry["title"]).weightedLength
        lim = max(min_len_title, current_len_title - difference)
        entry["title"] = simple(entry["title"], lim)

    return entry


# a simple text cut
def simple(orig, lim):
    orig = orig.strip()
    wlen = parse_tweet(orig).weightedLength
    if wlen <= lim:
        return orig

    while wlen > lim:
        orig = orig[:-1]
        wlen = parse_tweet(orig).weightedLength

    return orig[:-3] + "..."


# formating authors' names
def authors(orig, lim):
    if lim < 1:
        return ""
    if parse_tweet(orig).weightedLength <= lim:
        return orig

    collab = collaboration(orig)
    if collab != orig:
        if parse_tweet(collab).weightedLength <= lim:
            return collab
        else:
            return ""

    no_paren = noparen(orig)
    if parse_tweet(no_paren).weightedLength <= lim:
        return no_paren

    sr_names = surnames(no_paren)
    if parse_tweet(sr_names).weightedLength <= lim:
        return sr_names

    et_al = etal(no_paren)
    if parse_tweet(et_al).weightedLength <= lim:
        return et_al

    return ""


def collaboration(orig):
    collab = re.match(r"^[^:]+collaboration:", orig, re.IGNORECASE)
    if collab:
        return re.sub(":$", "", collab.group())
    else:
        return orig


def noparen(test_str):
    ret = ""
    skip = 0
    for i in test_str:
        if i == "(":
            skip += 1
        elif i == ")":
            skip -= 1
        elif skip == 0:
            ret += i
    ret = re.sub("[ ]+,", ",", ret)
    ret = re.sub("[ ]+$", "", ret)
    return ret


# cf. https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python/14598135#14598135


def surnames(orig):
    names = orig.split(",")
    sr_names = [HumanName(one).last or one.strip() for one in names]
    separator = ", "
    return separator.join(sr_names)


def etal(orig):
    names = orig.split(",")
    if len(names) > 1:
        return names[0].strip() + ", et al."
    return orig


# separate a text by weighted lengths <=lim
def separate(orig, lim):
    sep_text = []
    orig = orig.strip()

    # no inf loop
    if any(parse_tweet(t).weightedLength > lim for t in orig.split(" ")):
        print(
            "\n**cannot separate** \
        \nmax weighted length:  "
            + str(lim)
            + " \ninput:  "
            + orig
        )
        return sep_text

    while orig:
        partial_text = orig
        wlen = parse_tweet(partial_text).weightedLength
        while wlen > lim:
            partial_text = partial_text.rsplit(" ", 1)[0]
            wlen = parse_tweet(partial_text).weightedLength
        sep_text.append(partial_text.strip())
        orig = orig[len(partial_text) :].strip()
    return sep_text
