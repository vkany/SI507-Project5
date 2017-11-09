## import statements
from requests_oauthlib import OAuth2Session
from secret_data import app_id , app_secret, personal_token
import webbrowser
import json
from datetime import datetime

## CACHING SETUP

APP_ID = app_id
APP_SECRET = app_secret
AUTHORIZATION_BASE_URL = 'https://www.eventbrite.com/oauth/authorize'
TOKEN_URL = 'https://www.eventbrite.com/oauth/token'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
eb_session = False

## ADDITIONAL CODE for program should go here...
## Perhaps authentication setup, functions to get and process data, a class definition... etc.
# q = rawinput("What event would you like to attend?")
# if q = "" :
#     q = "Art Show"
# else:
#      q = q

# Set up sessions and so on to get data via OAuth2 protocol...
#
# oauth2inst = OAuth2Session(APP_ID, redirect_uri=REDIRECT_URI) # Create an instance of an OAuth2Session
#
# authorization_url, state = oauth2inst.authorization_url(AUTHORIZATION_BASE_URL) # all we need for spotify
#
# webbrowser.open(authorization_url) # Opening auth URL for you to sign in to the Spotify service
# authorization_response = input('Authenticate and then enter the full callback URL: ').strip() # Need to get the full URL in order to parse the response
#
# # The OAuth2Session instance has a method that extracts what we need from the url, and helps do some other back and forth with spotify
# token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=APP_SECRET)
## On a web server, this would happen on your server, but we have to pull the token out so we can use it for a request inside a script we're running on a personal computer (with connection to internet)
## Anytime we want to get new data we have to do this -- so a caching system would have to take this into account any time the data expired.
## And for that -- we'd want to think about the API rate limits, primarily!
# print(token)
def make_eb_request(url, params=None):
    # we use 'global' to tell python that we will be modifying this global variable
    global eb_session

    if not eb_session:
        start_eb_session()

    if not params:
        params = {}

    return eb_session.get(url, params=params)

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

# Now we can just use the get method on the oauth2session instance from here on out to make requests to spotify endpoints. Token will work for any endpoint, as long as it's still valid. (How long it is will depend from API to API)
API_BASE_URL = 'https://www.eventbriteapi.com/v3'
r = make_eb_request(API_BASE_URL + '/events/search/',params={
    'q': 'Art Show',
    'location.address': 'Detroit, MI'
})
response_diction = json.loads(r.text)
print(json.dumps(response_diction, indent=2))
# print(json.dumps(response_diction, indent=2))
## Make sure to run your code and write CSV files by the end of the program.
