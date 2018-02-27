import requests
import urllib2

from bs4 import BeautifulSoup
from fooda_creds import FOODA_EMAIL, FOODA_PW
from lxml import html

login_url = 'https://app.fooda.com/login'
session = requests.session()

# Get authenticity token for login.
# http://kazuar.github.io/scraping-tutorial/ is super helpful.
result = session.get(login_url)
tree = html.fromstring(result.text)
csrf_token = list(set(tree.xpath('//meta[@name="csrf-token"]/@content')))[0]

# Prepare login data, including token friend.
login_payload = {
    'user[email]': FOODA_EMAIL,
    'user[password]': FOODA_PW,
    'csrf-token': csrf_token,
}

# Do teh login.
result = session.post(
    login_url, data=login_payload, headers=dict(referer=login_url))
import pdb; pdb.set_trace()    
