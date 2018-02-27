import urllib2
import requests

from lxml import html
from bs4 import BeautifulSoup
from fooda_creds import FOODA_EMAIL, FOODA_PW, CSRF_TOKEN

login_dict = {
    'user[email]': FOODA_EMAIL,
    'user[password]': FOODA_PW,
    'csrf-token': CSRF_TOKEN,
}

session_requests = requests.session()
