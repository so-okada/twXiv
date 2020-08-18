#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a simple parser for arXiv new submission rss feeds
# a part of twXiv
# https://github.com/so-okada/twXiv/

import re
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse


class retrieve:
    def __init__(self, cat, aliases):
        url = 'http://export.arxiv.org/rss/' + cat
        resp = feedparser.parse(url)

        titles = []
        primary_subjects = []
        identifiers = []
        authors = []
        abstracts = []
        labels = []
        versions = []
        for each in resp.entries:
            title_subject = each['title'].split('. (arXiv:')
            titles.append(title_subject[0])

            # subjects
            current_identifier = re.findall('\[.*\]', title_subject[1])
            if current_identifier:
                subject = re.sub('[\[|\]]', '', current_identifier[0])
            else:
                old_identifier = re.findall('[-|\w]+\/', title_subject[1])
                subject = re.sub('/', '', old_identifier[0])
            subject = alias_replace(subject, aliases)

            # new submissions, cross-lists, or replacements
            primary_subjects.append(subject)
            if 'UPDATED' in title_subject[1]:
                labels.append('Replacement')
            elif 'CROSS LISTED' in title_subject[1]:
                labels.append('Cross-list')
            elif subject == cat:
                labels.append('New submission')
            else:
                labels.append('Cross-list')

            # versions
            versions.append(
                re.sub('v', '',
                       re.findall('v[0-9]+', title_subject[1])[0]))
            identifiers.append(re.sub('http://arxiv.org/abs/', '', each['id']))
            authors.append(BeautifulSoup(each['author'], 'lxml').text)
            abstracts.append(
                re.sub('\n', ' ',
                       BeautifulSoup(each['summary'], 'lxml').text))

        self.cat = cat
        self.feed = resp
        self.bozo = resp['bozo']
        self.entries = resp.entries
        self.updated = parse(resp['updated'])
        self.updated_parsed = datetime(*resp['updated_parsed'][:6])
        self.identifiers = identifiers
        self.authors = authors
        self.titles = titles
        self.labels = labels
        self.primary_subjects = primary_subjects
        self.abstracts = abstracts
        self.versions = versions

        # total number of new submissions/crosslists/replacements
        self.total = len(resp.entries)

        # metadata for new submissions/cross-lists/replacements
        newsubmissions = []
        crosslists = []
        replacements = []
        len_identifiers = len(self.identifiers)
        for each in range(len_identifiers):
            entry = {}
            entry['id'] = self.identifiers[each]
            entry['abs_url'] = 'https://arxiv.org/abs/' + entry['id']
            entry['pdf_url'] = re.sub('abs', 'pdf', entry['abs_url'])
            entry['title'] = self.titles[each]
            entry['authors'] = self.authors[each]
            entry['primary_subject'] = self.primary_subjects[each]
            entry['abstract'] = self.abstracts[each]
            entry['label'] = self.labels[each]
            entry['version'] = self.versions[each]
            # comments and subjects are not in feed 2020-07-12
            entry['comments'] = ''
            entry['subjects'] = ''

            if entry['label'] == 'New submission':
                newsubmissions.append(entry)
            elif entry['label'] == 'Cross-list':
                crosslists.append(entry)
            else:
                replacements.append(entry)

        self.newsubmissions = newsubmissions
        self.crosslists = crosslists
        self.replacements = replacements

        self.num_newsubmissions = len(newsubmissions)
        self.num_crosslists = len(crosslists)
        self.num_replacements = len(replacements)


def alias_replace(subject, aliases):
    if not aliases:
        return subject
    for i, j in aliases.items():
        if j == subject:
            return i
    return subject
