#!/usr/bin/env python
import datetime
import os
import sys
import random
import requests
import warnings

from bs4 import BeautifulSoup
from fooda_goodies import EMOJI_KEYWORDS, GREETINGS
from lxml import html

# First of all, let's be clear that this is dirty and horrible.
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# Sounds tricky, but turns out their user-visible login page submits
# to a create form, and THEN redirects you.
base_url = 'https://app.fooda.com/'
login_url = '{}/create'.format(base_url)
referrer_url = '{}/login'.format(base_url)
session = requests.session()

FOODA_EMAIL = os.environ.get('FOODA_EMAIL', None)
FOODA_PW = os.environ.get('FOODA_PW', None)
if not FOODA_EMAIL or not FOODA_PW:
    print('Check your creds!')
    sys.exit(1)

# Get authenticity token for login.
# http://kazuar.github.io/scraping-tutorial/ is super helpful.
get_token_result = session.get(login_url)
tree = html.fromstring(get_token_result.text)
auth_token = list(set(tree.xpath('//meta[@name="csrf-token"]/@content')))[0]

# Prepare login data, including token friend.
# These are the IDs of our fields...thanks, network tab!
login_payload = {
    'user[email]': FOODA_EMAIL,
    'user[password]': FOODA_PW,
    'authenticity_token': auth_token,
}

# Do teh login.
login_result = session.post(
    login_url, data=login_payload, headers=dict(referer=referrer_url))

# We are now on the default page for 100 Cambridge Park Drive.
#
# We will also want to construct URLs for our favorite buildings
# nearby, though - and we can get them from a dropdown on the page.
homepage_soup = BeautifulSoup(login_result.text)
dropdown_elm = homepage_soup.find('div', {'class': 'secondary-bar'})
links = [elm.get('href') for elm in dropdown_elm.find_all('a')]

print(u"{}\n".format(random.choice(GREETINGS)))
print(u"On this fine date of {}, you plebs may choose from:\n\n".format(
    datetime.date.today().strftime('%A, %d %B %Y')))

for link in links:
    foodpage_result = session.get(u'{}{}'.format(base_url, link))
    foodpage_soup = BeautifulSoup(foodpage_result.text)
    fooda_events = foodpage_soup.find_all(
        'div', {'class': 'myfooda-event__meta'})

    for event in fooda_events:
        location = unicode(event.find(
            'div', {'class': 'myfooda-event__meta-right myfooda-vendor-location-name'}).text.strip())
        vendor = event.find(
            'div', {'class': 'myfooda-event__meta-left'})
        vendor_name = unicode(vendor.find(
            'div', {'class': 'myfooda-event__name'}).text.strip())
        vendor_cuisines = unicode(vendor.find(
            'div', {'class': 'myfooda-event__cuisines'}).text.strip())
        # Possibly even add an emoji! :D
        cuisine_emoji = next(
            (emoji for kw, emoji in EMOJI_KEYWORDS.items() if kw in vendor_cuisines.lower()), None)
        if cuisine_emoji:
            vendor_cuisines = u'{} {}'.format(vendor_cuisines, cuisine_emoji)

        # Do what you want with this.
        print(u'{}\n'.format(location))
        print(u'       * {} ({})\n'.format(vendor_name, vendor_cuisines))
