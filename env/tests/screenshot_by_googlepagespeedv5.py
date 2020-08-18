#!/bin/env python3
""" Download a website screenshot using Google's PageSpeed API """
#https://stackoverflow.com/a/58686904
# https://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python
# updated for python3 and pagespeedonline v1->v5 2020-08-13
import re
import json
import base64
import requests

site = "https://arxiv.org/abs/2008.05469"

api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?screenshot=true&strategy=mobile"
# api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?screenshot=true&strategy=desktop"

r = requests.get(api, [('url', site)])
print(r)
site_data = r.json()
sc_encoded = site_data['lighthouseResult']['audits'][
    'final-screenshot']['details']['data']

# Google has a weird way of encoding the Base64 data
# screenshot_encoded = screenshot_encoded.replace("_", "/")
# screenshot_encoded = screenshot_encoded.replace("-", "+")
sc_decoded = base64.b64decode(re.sub('.*,', '', sc_encoded))

with open('screenshot.jpg', 'wb') as f:
    f.write(sc_decoded)
