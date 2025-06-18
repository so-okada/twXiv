#!/usr/bin/env python3
# written by So Okada so.okada@gmail.com
# a main interface of twXiv
# https://github.com/so-okada/twXiv/

import json
import argparse
import traceback
from twXiv_variables import *
import twXiv_post as tXp

parser = argparse.ArgumentParser(description="arXiv daily new submissions by tweets")
parser.add_argument(
    "--switches_keys",
    "-s",
    required=True,
    default="",
    help="output switches and api keys in json",
)
parser.add_argument("--logfiles", "-l", default="", help="log file names in json")
parser.add_argument(
    "--aliases", "-a", default="", help="aliases of arXiv categories in json"
)
parser.add_argument(
    "--captions", "-c", default="", help="captions of arXiv categories in json"
)
parser.add_argument(
    "--mode",
    "-m",
    choices=[0, 1],
    type=int,
    default="0",
    help="1 for twitter and 0 for stdout only",
)


args = parser.parse_args()
switches = args.switches_keys
logfiles = args.logfiles
aliases = args.aliases
captions = args.captions
pt_mode = args.mode


try:
    f = open(switches)
except Exception:
    traceback.print_exc()
    raise Exception("can not obtain output switches and api keys")
switches = json.load(f)

if logfiles:
    try:
        f = open(logfiles)
    except Exception:
        traceback.print_exc()
        raise Exception("can not obtain log filenames")
    logfiles = json.load(f)

if aliases:
    try:
        f = open(aliases)
    except Exception:
        traceback.print_exc()
        raise Exception("can not obtain aliases of arXiv categories")
    aliases = json.load(f)

if captions:
    try:
        f = open(captions)
    except Exception:
        traceback.print_exc()
        raise Exception("can not obtain captions of arXiv categories")
    captions = json.load(f)

tXp.main(switches, logfiles, captions, aliases, pt_mode)
