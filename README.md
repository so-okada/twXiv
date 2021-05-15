# Application Info

This application twXiv gives arXiv daily new submissions by tweets,
abstracts by replies, cross-lists by retweets, and replacements by
quotes and retweets.  We use python3 scripts. twXiv is not affiliated
with arXiv.


## Setup

* Install pandas, ratelimit, semanticscholar, tweepy, twitter-text-parser, nameparser, and beautifulsoup4. 

	```
	% pip3 install pandas ratelimit semanticscholar tweepy twitter-text-parser nameparser beautifulsoup4
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

*  arXiv_feed_parser.py is a simple arXiv feed parser for twXiv. We
	use this via twXiv_daily_feed.py to regularly obtain data.  
	
*	Output entries of twXiv can differ from those of arXiv new
	submission web pages. 
	First, under our current settings, arXiv_feed_parser of a
	category C gives new submissions whose primary subjects are the
	category C.	Second, entries of arXiv rss feeds are not
	necessarily the same as those of arXiv new submission web pages.


* 	On the use of metadata of arXiv articles, there is the web page of
   [Terms of Use for arXiv APIs](https://arxiv.org/help/api/tou). As
   of the revision 0.8.0, this says "You are free to use descriptive
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


## Version history

* 0.0.1

  * 2020-08-08, initial release.
  
* 0.0.2

  * 2020-08-15, added the -c option.

* 0.1.0

  * 2021-01-31, text counting by twitter-text-parser, replacements by
	quotes and retweets, and links to research tools.

* 0.1.1

  * 2021-03-02, minor fixes.

## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation

Since 2013-04, the author has been running arXiv bots

* [https://twitter.com/mathACb](https://twitter.com/mathACb)
* [https://twitter.com/mathAGb](https://twitter.com/mathAGb)
* ...
* [https://twitter.com/mathSTb](https://twitter.com/mathSTb)

for all arXiv math categories  (see 
[a paper on these bots](https://arxiv.org/abs/1410.4139)
and  [the author's comment](https://twitter.com/vela/status/729622960974127104)). 
The bots used arxiv_speaker [https://github.com/misho104-obsolete/arxiv_speaker](https://github.com/misho104-obsolete/arxiv_speaker). Sho Iwamoto wrote it by ruby for tweeting new submissions. 
However, it has been
discontinued for a while. Therefore, the author has written twXiv
by python3, adding functions such as abstracts by replies,
cross-lists by retweets, and replacements by quotes and retweets. 
Since 2020-08, the bots run by twXiv.

 



## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

