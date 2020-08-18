#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a part of twXiv for formatting arXiv metadata
# https://github.com/so-okada/twXiv/

import re
from nameparser import HumanName
from variables import *


# format all new submissions
def format(entries):
    return [format_each(one) for one in entries]


# format each new submission
def format_each(orig_entry):
    fixed_length = urls_len + newsub_spacer + margin
    entry = orig_entry.copy()
    orig_title = entry['title']
    current_len = \
        len(entry['authors'] + entry['title']) + fixed_length
    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = len(entry['title'])
        lim = max(min_len_title, current_len_title - difference)
        entry['title'] = simple(entry['title'], lim)

    current_len = \
        len(entry['authors'] + entry['title']) + fixed_length
    if current_len > max_len:
        difference = current_len - max_len
        current_len_authors = len(entry['authors'])
        lim = max(min_len_authors, current_len_authors - difference)
        entry['authors'] = authors(entry['authors'], lim)

    # The following step tries to take a longer title
    # when the length of authors' names becomes shorter
    entry['title'] = orig_title
    current_len = \
        len(entry['authors'] + entry['title']) + fixed_length
    if current_len > max_len:
        difference = current_len - max_len
        current_len_title = len(entry['title'])
        lim = max(min_len_title, current_len_title - difference)
        entry['title'] = simple(entry['title'], lim)

    entry['separated_abstract'] = \
        separate_abstract(entry['abstract'], entry['id'],
                          max_len - abst_tag - margin)
    return entry


# a simple text cut
def simple(orig, lim):
    len_original = len(orig)
    if len_original <= lim:
        return orig
    else:
        return orig[:lim - 3] + "..."


# formating authors' names
def authors(orig, lim):
    if lim < 1:
        return ''
    if len(orig) <= lim:
        return orig

    collab = collaboration(orig)
    if collab != orig:
        if len(collab) <= lim:
            return collab
        else:
            return ''

    no_paren = noparen(orig)
    if len(no_paren) <= lim:
        return no_paren

    sr_names = surnames(no_paren)
    if len(sr_names) <= lim:
        return sr_names

    et_al = etal(no_paren)
    if len(et_al) <= lim:
        return et_al

    return ''


def collaboration(orig):
    collab = re.match(r'^[^:]+collaboration:', orig, re.IGNORECASE)
    if collab:
        return re.sub(':$', '', collab.group())
    else:
        return orig

    
def noparen(test_str):
    ret = ''
    skip = 0
    for i in test_str:
        if i == '(':
            skip += 1
        elif i == ')':
            skip -= 1
        elif skip == 0:
            ret += i
    ret = re.sub('[ ]+,', ',', ret)
    ret = re.sub('[ ]+$', '', ret)
    return ret
# cf. https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python/14598135#14598135


def surnames(orig):
    names = orig.split(',')
    sr_names = [HumanName(one).last for one in names]
    separator = ', '
    return separator.join(sr_names)


def etal(orig):
    first_author = re.search(r'[\w|.| ]+,', orig)
    return first_author.group() + " et al."


# separate an abstract with a counter and url tag
def separate_abstract(orig, id, lim):
    sep_abstract = separate(orig, lim)
    num = len(sep_abstract)
    result = []
    for i, each in enumerate(sep_abstract):
        ptext = each + \
            "[" + str(i+1) + "/" + str(num) + \
            " of https://arxiv.org/abs/"+id+"v1]"
        result.append(ptext)
    return result


# separate a text by lengths <=lim
def separate(orig, lim):
    sep_text = []
    if len(orig) <= lim:
        sep_text.append(orig)
        return sep_text
    while len(orig) > lim:
        partial_text = orig[:lim]
        last_word = re.findall(r'[ ]{1}[^ ]+$', partial_text)
        if last_word:
            last_word = re.findall('[ ]{1}[^ ]+$', partial_text)[0]
            partial_text = orig[:lim - (len(last_word) - 1)]
        sep_text.append(partial_text)
        orig = orig[len(partial_text):]
    sep_text.append(orig)
    return sep_text



