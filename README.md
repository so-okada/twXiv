# Application Info

This application twXiv gives arXiv daily new submissions by tweets. 
We use python3 scripts. twXiv is not affiliated with arXiv.


## Setup

* Install pandas, ratelimit, tweepy, twitter-text-parser, nameparser, and feedparser.

	```
	% pip3 install pandas ratelimit tweepy twitter-text-parser nameparser feedparser 
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
	- arXiv_feed_parser.py
	- twXiv_variables.py


* Configure switches.json, logfiles.json, and aliases.json in the
  tests directory for your settings.

	- accesses.json specifies twitter access keys and whether to put
	new submissions for each category.

    - logfiles.json indicates log file locations for tweet summaries
	and tweets. In the tests/logfiles director, you have the sample
	log files mathACb_tweet_summaries.csv and mathACb_tweets.csv.
		
	- aliases.json tells twXiv aliases of arXiv category names.  For
    example, math.IT is an alias of cs.IT.  If provided, twXiv
    replaces category names by their aliases.
	
* Configure twXiv_variables.py for your settings. 

   - twXiv_variables.py assigns format parameters for twXiv tweets 
   and access frequencies for arXiv and twitter.

## Notes

* arXiv_feed_parser.py is a simple arXiv feed parser for twXiv. We
  use this via twXiv_daily_feed.py to regularly obtain data. 
	
* Outputs of twXiv can differ from arXiv new submission web
  pages. First, this can be due to bugs in my scripts or connection
  errors.  Second, items of arXiv rss feeds are not necessarily the
  same as those of arXiv new submission web pages (see
  https://mastoxiv.page/@vela/109829294232368163).  Third,
  arXiv_feed_parser for an arXiv category C gives new submissions
  whose primary subjects are the category C.  Then, twXiv for the
  category C counts and tweets a new paper whose principal subject
  matches the category C.

	- For example, let us assume that there is no new paper whose
	principal subject matches the category C, but there is a new paper
	P whose non-principal subject matches the category C. Then, the
	arXiv new submission web page of the category C lists the paper P
	as a new submission of the category C, not as a cross-list.
	However, twXiv keeps considering the paper P as a cross-list for
	the category C.  Then, the output of twXiv for the category C
	differs from the arXiv new submission web page of the category C.
	One reason for this is to clarify what twXiv tweets across
	categories.  Another reason is that twitter does not like
	duplicate or substantially similar tweets for bots.


* On the use of metadata of arXiv articles, there is the web page of
   [Terms of Use for arXiv APIs](https://arxiv.org/help/api/tou). 
   This says that "You are free to use descriptive
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

arXiv daily new submissions by tweets.

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

* New submissions (if any)   for math.AC and math.AG:
	```
	% ./twXiv.py -s tests/switches.json -l tests/logfiles.json -a tests/aliases.json -c tests/captions.json -m 1
	**process started at xxxx-xx-xx xx:xx:xx (UTC)
	starting a thread of retrieval/new submissions for math.AC
	getting daily entries for math.AC
	waiting for a next thread of retrieval/new submissions
	new submissions for math.AC

	utc: xxxx-xx-xx xx:xx:xx 
	thread arXiv category: math.AC
	arXiv id: 
	url: https://x.com/user/status/
	post method: tweet
	post mode: 1
	url: https://x.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 2 new articles found for mathAC Commutative Algebra]

	starting a thread of retrieval/new submissions for math.AG
	getting daily entries for math.AG
	joining threads of retrieval/new submissions

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AC
	arXiv id: 2007.xxxxxx
	url: https://x.com/user/status/
	post method: tweet
	post mode: 1
	url: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

	new submissions for math.AG

	utc: xxxx-xx-xx xx:xx:xx
	thread arXiv category: math.AG
	arXiv id: 
	url: https://x.com/user/status/
	post method: tweet
	post mode: 1
	url: https://x.com/user/status/xxxxxxxxxxxxxxxxxxxxxxxxxxxx
	text: [xxxx-xx-xx Sun (UTC), 4 new articles found for mathAG Algebraic Geometry]
	.....

	** process ended at xxxx-xx-xx xx:xx:xx (UTC)
	** elapsed time from the start: xx:xx:xx
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

	* 2021-06-03, a fix for semantic scholar api update.
	
* 0.1.3

	* 2021-10-26, a fix for tweepy v4.

* 0.1.4

	* 2022-08-20, minor fixes.
	
* 0.1.5
	
	* 2022-01-09, a fix for semanticscholar 0.3.2.
	
* 0.2.0	
		
	* 2023-06-25, a fix for twitter API V2 endpoints and a daily rate limit.

* 0.3.0	

	* 2024-02-04, updated arXiv_feed_parser for arXiv rss re-implemented.
	
* 0.3.1	

	* 2024-02-07, a minor update.
	
* 0.4.1

	* 2025-01-12, deleted functions of retweets and replies for the X free api limits,
	updated for the X api "17 posts a day" limit by a tweet of two papers,
	added https://en.wikipedia.org/wiki/Mathematics as a generic math page
	for an automatic url preview of the two paper tweets, and
	added html paper links.
	
* 0.4.2

	* 2026-02-18, fixes for name handling.
	
## List of Bots

* [https://x.com/mathACb](https://x.com/mathACb): 
  Commutative Algebra
* [https://x.com/mathAGb](https://x.com/mathAGb):
  Algebraic Geometry
* [https://x.com/mathAPb](https://x.com/mathAPb):
  Analysis of PDEs 
* [https://x.com/mathATb](https://x.com/mathATb):
Algebraic Topology 
* [https://x.com/mathCAbot](https://x.com/mathCAbot):
Classical Analysis and ODEs
* [https://x.com/mathCObot](https://x.com/mathCObot):
Combinatorics 
* [https://x.com/mathCTbot](https://x.com/mathCTbot):
Category Theory 
* [https://x.com/mathCVb](https://x.com/mathCVb):
Complex Variables 
* [https://x.com/mathDGb](https://x.com/mathDGb):
Differential Geometry 
* [https://x.com/mathDSb](https://x.com/mathDSb):
Dynamical Systems 
* [https://x.com/mathFAbot](https://x.com/mathFAbot):
Functional Analysis 
* [https://x.com/mathGMb](https://x.com/mathGMb):
General Mathematics 
* [https://x.com/mathGNb](https://x.com/mathGNb):
General Topology 
* [https://x.com/mathGRbot](https://x.com/mathGRbot):
Group Theory 
* [https://x.com/mathGTb](https://x.com/mathGTb):
Geometric Topology 
* [https://x.com/mathHOb](https://x.com/mathHOb):
History and Overview 
* [https://x.com/mathITbot](https://x.com/mathITbot):
Information Theory 
* [https://x.com/mathKTb](https://x.com/mathKTb):
K-Theory and Homology 
* [https://x.com/mathLOb](https://x.com/mathLOb):
Logic 
* [https://x.com/mathMGb](https://x.com/mathMGb):
Metric Geometry 
* [https://x.com/mathMPb](https://x.com/mathMPb):
Mathematical Physics 
* [https://x.com/mathNAb](https://x.com/mathNAb):
Numerical Analysis 
* [https://x.com/mathNTb](https://x.com/mathNTb):
Number Theory 
* [https://x.com/mathOAb](https://x.com/mathOAb):
Operator Algebras 
* [https://x.com/mathOCb](https://x.com/mathOCb):
Optimization and Control 
* [https://x.com/mathPRb](https://x.com/mathPRb):
Probability
* [https://x.com/mathQAb](https://x.com/mathQAb):
Quantum Algebra 
* [https://x.com/mathRAb](https://x.com/mathRAb):
Rings and Algebras
* [https://x.com/mathRTb](https://x.com/mathRTb):
Representation Theory 
* [https://x.com/mathSGb](https://x.com/mathSGb):
Symplectic Geometry 
* [https://x.com/mathSPb](https://x.com/mathSPb):
Spectral Theory 
* [https://x.com/mathSTb](https://x.com/mathSTb):
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
 replacements by quotes and retweets. 
Since 2020-08, the
 bots above have used twXiv on gcp free tier.
 Since 2025-01, the author has 
 added the function of  two-new-submissions-in-one-tweet
 and abondoned
 the functions of abstracts, cross-lists, and replacements
 for the limitations of  X api free tire.


For more background, see 
[a paper on these bots](https://arxiv.org/abs/1410.4139),
 [bots](https://dicto.xyz/bookmarks/arxiv-twitter-feeds/)
of
[Notionsandnotes](https://twittercommunity.com/u/notionsandnotes/summary), and
the author's
comments:
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I am running these bots mainly just for convenience of sharing wisdom of arXiv papers for each arXiv category.</p>&mdash; So Okada (@vela) <a href="https://x.com/vela/status/729622960974127104?ref_src=twsrc%5Etfw">May 9, 2016</a></blockquote> 
<!-- <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script> -->
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">This would end my 32 math arXiv twitter bots such as <a href="https://t.co/w8cCIaUlBM">https://t.co/w8cCIaUlBM</a>, <a href="https://t.co/2j62N9Vk8a">https://t.co/2j62N9Vk8a</a>, ... They have shared wisdom of arXiv papers with comments, discussions, or jokes not just to academics but to the public. I have maintained them nearly 10 years from 2013-04. <a href="https://t.co/J0WUSSTlwZ">https://t.co/J0WUSSTlwZ</a></p>&mdash; So Okada (@vela) <a href="https://x.com/vela/status/1622129115603308544?ref_src=twsrc%5Etfw">February 5, 2023</a></blockquote>
<!-- <script async src="https://platform.x.com/widgets.js" charset="utf-8"></script> -->


## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


