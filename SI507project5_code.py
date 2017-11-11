## import statements:

from requests_oauthlib import OAuth2Session
from secret_data import app_id , app_secret
import webbrowser
import json
from datetime import datetime
import csv

## CACHING SETUP
APP_ID = app_id
APP_SECRET = app_secret
AUTHORIZATION_BASE_URL = 'https://www.eventbrite.com/oauth/authorize'
TOKEN_URL = 'https://www.eventbrite.com/oauth/token'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
eb_session = False
CACHE_DICTION = {}
CACHE_FNAME = 'cached_event_list.json'

# caching
def load_cache():
    global CACHE_DICTION
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

def save_cache():
    full_text = json.dumps(CACHE_DICTION)
    cache_file_ref = open(CACHE_FNAME,"w")
    cache_file_ref.write(full_text)
    cache_file_ref.close()

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def make_eb_request(url, params=None):
    # we use 'global' to tell python that we will be modifying this global variable
    global eb_session

    if not params:
        params = {}

    unique_ident = params_unique_combination(url, params)

    # if not in cache, get fresh data
    if unique_ident not in CACHE_DICTION:
        if not eb_session:
            start_eb_session()

        response = eb_session.get(url, params=params)
        # response = requests.get(baseurl, params=params)
        CACHE_DICTION[unique_ident] = json.loads(response.text)
        save_cache()
        print('--> fresh copy')
    else:
        print('--> cached')

    return CACHE_DICTION[unique_ident]

def start_eb_session():
    global eb_session


    # 0 - get token from cache
    try:
        token = get_saved_token()
    except FileNotFoundError:
        token = None

    if token:
        eb_session = OAuth2Session(APP_ID, token=token)

    else:
        # 1 - session
        eb_session = OAuth2Session(APP_ID, redirect_uri=REDIRECT_URI)

        # 2 - authorization
        authorization_url, state = eb_session.authorization_url(AUTHORIZATION_BASE_URL)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)

        # 3 - token
        redirect_response = input('Paste the full redirect URL here: ')
        token = eb_session.fetch_token(TOKEN_URL, client_secret=APP_SECRET,
            authorization_response=redirect_response.strip())

        # 4 - save token
        save_token(token)

def get_saved_token():
    with open('token.json', 'r') as eb:
        token_json = eb.read()
        token_dict = json.loads(token_json)
        return token_dict

def save_token(token_dict):
    with open('token.json', 'w') as f:
        token_json = json.dumps(token_dict)
        f.write(token_json)

load_cache()

# Now we can just use the get method on the oauth2session instance from here on out to make requests to spotify endpoints. Token will work for any endpoint, as long as it's still valid. (How long it is will depend from API to API)
API_BASE_URL = 'https://www.eventbriteapi.com/v3'
def get_response_diction(query,location):
    return make_eb_request(API_BASE_URL + '/events/search/',params={
    'q': query,
    'location.address': location,
    'sort_by':'-date',
    'start_date.keyword':'this_week'
    })


det_music = get_response_diction('Music Concerts','Detroit')
ny_art = get_response_diction('Art Show','New York')
# print(json.dumps(get_response_diction('Art Show','New York'), indent=2))
# print(json.dumps(get_response_diction('Music Concerts','Detroit'), indent=2))
# def filter_details(diction):
#     for event in diction["events"]:
#         name = event["name"]["text"]
#         time = event["start"]["local"]
#         description = event["description"]["text"]
#         url = event["resource_uri"]
#     details= [name, time, description,url]
#     return details
#
# print(filter_details(det_music))


with open("Detroit_Music_Events.csv", 'w', newline='') as concerts_list:
    writer = csv.writer(concerts_list)
    concerts_list.write("Event Name, Time, Description, Event URL\n")
    for event in det_music["events"]:
        writer.writerow([event["name"]["text"],event["start"]["local"], event["description"]["text"],event["url"]])

with open("NY_Art_Events.csv", 'w', newline='') as artshows_list:
    writer = csv.writer(artshows_list)
    artshows_list.write("Event Name, Time, Description, Event URL\n")
    for event in ny_art["events"]:
        writer.writerow([event["name"]["text"],event["start"]["local"], event["description"]["text"],event["url"]])
