# Application Info

This application twXiv gives arXiv daily new submissions by tweets,
abstracts by replies, cross-lists by retweets, and replacements by
quotes and retweets.  We use python3 scripts. twXiv is not affiliated
with arXiv.


## Setup

* Install pandas, ratelimit, semanticscholar, tweepy, twitter-text-parser, nameparser, feedparser, and beautifulsoup4. 

	```
	% pip3 install pandas ratelimit semanticscholar tweepy twitter-text-parser nameparser feedparser beautifulsoup4
	```

* Let twXiv.py be executable.
 
	 ```
	 % chmod +x twXiv.py
	 ```

*  Put the following python scripts in the same directory.

	- twXiv.py
	- twXiv_post.py 	
	- twXiv_format.py
	- twXiv_daily_feed.py 	
	- twXiv_semantic.py
	- arXiv_feed_parser.py
	- variables.py


* Configure switches.json, logfiles.json, and aliases.json in the
  tests directory for your settings.

	- accesses.json specifies twitter access keys and whether to use
	new submissions/abstracts/cross-lists/replacements by twXiv.

    - logfiles.json indicates log file locations for tweet summaries,
	tweets, retweets, unretweets, and replies.  You can check their
	formats by mathACb_tweet_summaries.csv, mathACb_tweets.csv,
	mathACb_retweets.csv, mathACb_unretweets.csv, 
	mathACb_replies.csv,
	and mathACb_quotes.csv in the tests/logfiles director.  twXiv
	needs a tweet log file for cross-lists and replacements.  Other
	log files are useful to avoid duplication errors of tweets and
	retweets.
		
	- aliases.json tells twXiv aliases of arXiv category names.
    For example, math.IT is an alias of cs.IT. Without  this file,
	twXiv of rss feeds returns no 
	new submissions,
	when you take the category name math.IT. 
	If provided, twXiv replaces category names by their aliases
	for new submissions, cross-lists, and replacements.
	
* Configure variables.py for your settings. 

   - variables.py assigns format parameters for twXiv tweets 
   and access frequencies for arXiv and twitter.

## Notes

* arXiv_feed_parser.py is a simple arXiv feed parser for twXiv. We
  use this via twXiv_daily_feed.py to regularly obtain data.  
	
* Outputs of twXiv can differ from arXiv new submission web
  pages. First, this can be due to bugs in my scripts or
  connection errors.
  Second, items of arXiv rss feeds are not
  necessarily the same as those of arXiv new submission web
  pages (see
	https://mastoxiv.page/@vela/109829294232368163).  Third,
  arXiv_feed_parser for an arXiv category C gives new
  submissions whose primary subjects are the category C.
  Then, twXiv for the category C counts and tweets a new
  paper whose principal subject matches the category C.

	- For example, let us assume that there is no new paper whose
	principal subject matches the category C, but there is a
	new paper P whose non-principal subject matches the
	category C. Then, the arXiv new submission web page of
	the category C lists the paper P as a new submission of
	the category C, not as a cross-list.  However, twXiv
	keeps considering the paper P as a cross-list for the
	category C.  Then, the output of twXiv for the category
	C differs from the arXiv new submission web page of the
	category C.

	- One reason for this is to clarify what twXiv tweets,
	retweets, and quotes across categories.  Another reason
	is that twitter does not like duplicate or
	substantially similar tweets from bots.  So, twXiv
	maintains a single tweet for the title, authors, and
	abs/pdf identifiers of a new paper across bots in 
	access keys. Furthermore, if configured, twXiv tries to
	retweet and quote for cross-lists and replacements from
	bots in access keys.


* On the use of metadata of arXiv articles, there is the web page of
   [Terms of Use for arXiv APIs](https://arxiv.org/help/api/tou). As
   of the revision 0.8.0, this says that "You are free to use descriptive
   metadata about arXiv e-prints under the terms of the Creative
   Commons Universal (CC0 1.0) Public Domain Declaration." and
   "Descriptive metadata includes information for discovery and
   identification purposes, and includes fields such as title,
   abstract, authors, identifiers, and classification terms."


## Usage

```
% ./twXiv.py -h
usage: twXiv.py [-h] --switches_keys SWITCHES_KEYS
                [--logfiles LOGFILES] [--aliases ALIASES]
                [--captions CAPTIONS] [--mode {0,1}]

arXiv daily new submissions by tweets, abstracts by
replies, cross-lists by retweets, and replacements by
quotes and retweets.

optional arguments:
  -h, --help            show this help message and exit
  --switches_keys SWITCHES_KEYS, -s SWITCHES_KEYS
                        output switches and api keys in
                        json
  --logfiles LOGFILES, -l LOGFILES
                        log file names in json
  --aliases ALIASES, -a ALIASES
                        aliases of arXiv categories in
                        json
  --captions CAPTIONS, -c CAPTIONS
                        captions of arXiv categories in
                        json
  --mode {0,1}, -m {0,1}
                        1 for twitter and 0 for stdout
                        only
```

## Sample stdouts


* New submissions for math.AC and math.AG with no log files:

	```
	% ./twXiv.py -s tests/switches.json -m 1
	**process started at xxxx-xx-xx xx:xx:xx (UTC)
	starting a thread of retrieval/new submissions/abstracts for math.AC
	getting daily entries for math.AC
	waiting for a next thread of retrieval/new submissions/abstracts
	new submissions for math.AC
	no log files
	no log files

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AC
	arXiv id: 
	url: https://twitter.com/user/status/
	post method: tweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 2 new articles found for mathAC]

	starting a thread of retrieval/new submissions/abstracts for math.AG
	getting daily entries for math.AG
	joining threads of retrieval/new submissions/abstracts

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: xxxx.xxxxx
	url: https://twitter.com/user/status/
	post method: tweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxx
	text: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	....

	**process ended at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	```

* New submissions, abstracts, cross-lists and replacements (if any) 
  for math.AC and math.AG:

	```
	% ./twXiv.py -s tests/switches.json -l tests/logfiles.json -a tests/aliases.json -c tests/captions.json -m 1
	**process started at xxxx-xx-xx xx:xx:xx (UTC)
	starting a thread of retrieval/new submissions/abstracts for math.AC
	getting daily entries for math.AC
	waiting for a next thread of retrieval/new submissions/abstracts
	new submissions for math.AC

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AC
	arXiv id: 
	url: https://twitter.com/user/status/
	post method: tweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 2 new articles found for mathAC Commutative Algebra]

	starting a thread of retrieval/new submissions/abstracts for math.AG
	getting daily entries for math.AG
	joining threads of retrieval/new submissions/abstracts

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: 2007.xxxxxx
	url: https://twitter.com/user/status/
	post method: tweet
	post mode: 1
	url: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	new submissions for math.AG

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AG
	arXiv id: 
	url: https://twitter.com/user/status/
	post method: tweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG Algebraic Geometry]

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: 2007.xxxxxx
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	post method: reply
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	text:  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx [1/4 of https://arxiv.org/abs/2007.xxxxxv1]

	.....
	
	**crosslist process started at xxxx-xx-xx xx:xx:xx (UTC) 
	**elapsed time from the start: xx:xx:xx
	start a crosslist thread of math.AC
	waiting for a next crosslist thread
	start a crosslist thread of math.AG
	joining crosslist threads

	**replacement process started at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	**elapsed time from the cross-list start: xx:xx:xx
	quote-replacement starts
	start a quote-replacement thread of math.AC
	waiting for a next quote-replacement thread
	start a quote-replacement thread of math.AG
	
	.....
	
	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AG
	arXiv id: 2010.xxxx
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	post method: quote
	post mode: 0
	url: https://twitter.com/user/status/
	text: This https://arxiv.org/abs/xxxx.xxxx has been replaced.....

	.....

	retweet-replacement starts
	start a retweet-replacement thread of math.AC
	waiting for a next quote-replacement thread
	start a retweet-replacement thread of math.AG
	
	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AG
	arXiv id: 1900.xxxxx
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	post method: unretweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	text: 

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AG
	arXiv id: 1900.xxxxx
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	post method: retweet
	post mode: 1
	url: https://twitter.com/user/status/xxxxxxxxxxxxxxxxxxxx
	text: 

	.....

	**process ended at xxxx-xx-xx xx:xx:xx (UTC)
	**elapsed time from the start: xx:xx:xx
	**elapsed time from the cross-list start: xx:xx:xx
	**elapsed time from the replacement start: xx:xx:xx
	```
* Without the option ```-c tests/captions.json```above, you get

	```
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG]
	```

	instead of

	```
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG Algebraic Geometry]
	```


## Versions

* 0.0.1

  * 2020-08-08, initial release.
  
* 0.0.2

  * 2020-08-15, added the -c option.

* 0.1.0

  * 2021-01-31, text counting by twitter-text-parser, replacements by
	quotes and retweets, and links to research tools.

* 0.1.1

	* 2021-03-02, minor fixes.
  
* 0.1.2

	* 2021-06-03, a fix to adapt an api update of semantic scholar.
	
* 0.1.3

	* 2021-10-26,  a fix for tweepy v4.

* 0.1.4

	* 2022-08-20, minor fixes.
	
* 0.1.5
	
	* 2022-01-09, a fix for semanticscholar 0.3.2.
		
## List of Bots

* [https://twitter.com/mathACb](https://twitter.com/mathACb): 
  Commutative Algebra
* [https://twitter.com/mathAGb](https://twitter.com/mathAGb):
  Algebraic Geometry
* [https://twitter.com/mathAPb](https://twitter.com/mathAPb):
  Analysis of PDEs 
* [https://twitter.com/mathATb](https://twitter.com/mathATb):
Algebraic Topology 
* [https://twitter.com/mathCAbot](https://twitter.com/mathCAbot):
Classical Analysis and ODEs
* [https://twitter.com/mathCObot](https://twitter.com/mathCObot):
Combinatorics 
* [https://twitter.com/mathCTbot](https://twitter.com/mathCTbot):
Category Theory 
* [https://twitter.com/mathCVb](https://twitter.com/mathCVb):
Complex Variables 
* [https://twitter.com/mathDGb](https://twitter.com/mathDGb):
Differential Geometry 
* [https://twitter.com/mathDSb](https://twitter.com/mathDSb):
Dynamical Systems 
* [https://twitter.com/mathFAbot](https://twitter.com/mathFAbot):
Functional Analysis 
* [https://twitter.com/mathGMb](https://twitter.com/mathGMb):
General Mathematics 
* [https://twitter.com/mathGNb](https://twitter.com/mathGNb):
General Topology 
* [https://twitter.com/mathGRbot](https://twitter.com/mathGRbot):
Group Theory 
* [https://twitter.com/mathGTb](https://twitter.com/mathGTb):
Geometric Topology 
* [https://twitter.com/mathHOb](https://twitter.com/mathHOb):
History and Overview 
* [https://twitter.com/mathITbot](https://twitter.com/mathITbot):
Information Theory 
* [https://twitter.com/mathKTb](https://twitter.com/mathKTb):
K-Theory and Homology 
* [https://twitter.com/mathLOb](https://twitter.com/mathLOb):
Logic 
* [https://twitter.com/mathMGb](https://twitter.com/mathMGb):
Metric Geometry 
* [https://twitter.com/mathMPb](https://twitter.com/mathMPb):
Mathematical Physics 
* [https://twitter.com/mathNAb](https://twitter.com/mathNAb):
Numerical Analysis 
* [https://twitter.com/mathNTb](https://twitter.com/mathNTb):
Number Theory 
* [https://twitter.com/mathOAb](https://twitter.com/mathOAb):
Operator Algebras 
* [https://twitter.com/mathOCb](https://twitter.com/mathOCb):
Optimization and Control 
* [https://twitter.com/mathPRb](https://twitter.com/mathPRb):
Probability
* [https://twitter.com/mathQAb](https://twitter.com/mathQAb):
Quantum Algebra 
* [https://twitter.com/mathRAb](https://twitter.com/mathRAb):
Probability 
* [https://twitter.com/mathRTb](https://twitter.com/mathRTb):
Representation Theory 
* [https://twitter.com/mathSGb](https://twitter.com/mathSGb):
Symplectic Geometry 
* [https://twitter.com/mathSPb](https://twitter.com/mathSPb):
Spectral Theory 
* [https://twitter.com/mathSTb](https://twitter.com/mathSTb):
Statistics Theory 

## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation

Since 2013-04, the author has been running the bots above
 for all arXiv math categories.  Until 2020-08, the author
 used arxiv_speaker
 [https://github.com/misho104-obsolete/arxiv_speaker](https://github.com/misho104-obsolete/arxiv_speaker). Sho
 Iwamoto wrote it by ruby for tweeting new submissions with
 titles, authors, and ids.  However, it was
 discontinued.  Therefore, the author has
 written twXiv by python3, adding functions such as
 abstracts by replies, cross-lists by retweets, and
 replacements by quotes and retweets.  Since 2020-08, the
 bots above have used twXiv on gcp free tier.

For more background, see 
[a paper on these bots](https://arxiv.org/abs/1410.4139),
 [bots](https://dicto.xyz/bookmarks/arxiv-twitter-feeds/)
of
[Notionsandnotes](https://twittercommunity.com/u/notionsandnotes/summary), and
the author's
comments:
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I am running these bots mainly just for convenience of sharing wisdom of arXiv papers for each arXiv category.</p>&mdash; So Okada (@vela) <a href="https://twitter.com/vela/status/729622960974127104?ref_src=twsrc%5Etfw">May 9, 2016</a></blockquote> 
<!-- <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> -->
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">This would end my 32 math arXiv twitter bots such as <a href="https://t.co/w8cCIaUlBM">https://t.co/w8cCIaUlBM</a>, <a href="https://t.co/2j62N9Vk8a">https://t.co/2j62N9Vk8a</a>, ... They have shared wisdom of arXiv papers with comments, discussions, or jokes not just to academics but to the public. I have maintained them nearly 10 years from 2013-04. <a href="https://t.co/J0WUSSTlwZ">https://t.co/J0WUSSTlwZ</a></p>&mdash; So Okada (@vela) <a href="https://twitter.com/vela/status/1622129115603308544?ref_src=twsrc%5Etfw">February 5, 2023</a></blockquote>
<!-- <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> -->


## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


