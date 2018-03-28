import requests

from bs4 import BeautifulSoup
from fooda_creds import FOODA_EMAIL, FOODA_PW
from lxml import html

# Sounds tricky, but turns out their user-visible login page submits
# to a create form, and THEN redirects you.
login_url = 'https://app.fooda.com/create'
referrer_url = 'https://app.fooda.com/login'
session = requests.session()

# Get authenticity token for login.
# http://kazuar.github.io/scraping-tutorial/ is super helpful.
result = session.get(login_url)
tree = html.fromstring(result.text)
auth_token = list(set(tree.xpath('//meta[@name="csrf-token"]/@content')))[0]

# Prepare login data, including token friend.
# These are the IDs of our fields...thanks, network tab!
login_payload = {
    'user[email]': FOODA_EMAIL,
    'user[password]': FOODA_PW,
    'authenticity_token': auth_token,
}

# Do teh login.
result = session.post(
    login_url, data=login_payload, headers=dict(referer=referrer_url))

# We are now on the default page for 100 Cambridge Park Drive.
#
# We will also want to construct URLs for our favorite buildings
# nearby, though - and we can get them from a dropdown on the page.
soup = BeautifulSoup(result.text)
dropdownElm = soup.find('div', {'class': 'secondary-bar'})
links = [elm.get('href') for elm in dropdownElm.find_all('a')]
import pdb; pdb.set_trace()    
