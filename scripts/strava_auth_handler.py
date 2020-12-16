'''
Simple Script for getting the Access token

Set up a client using stravalib
If prompted enter client ID and client secret from https://www.strava.com/settings/api
Upon authorisation, retrieve the 'code=' section of the url and input when prompted
'''
import json
import os
import webbrowser
import argparse
import time
from stravalib.client import Client

def parse_args(args):
    access_token_file_name = args.output_file

    client = Client()
    access_token_does_exist = os.path.isfile(access_token_file_name)
    access_token_doesnt_exist = not(access_token_does_exist)
    access_token_expired = True

    if access_token_does_exist:
         with open(access_token_file_name, 'r') as f:
            token_response = json.load(f)
            token_response = json.loads(token_response)
            token_expiry_time = token_response['expires_at']
            current_time = time.time()
            access_token_expired = current_time > token_expiry_time

    if access_token_doesnt_exist or access_token_expired:
        client_id = args.client_id
        client_secret = args.client_secret
        scope = ['read', 'read_all', 'profile:read_all', 'activity:read', 'activity:read_all']
        authorize_url = client.authorization_url(client_id=client_id, redirect_uri='http://localhost:5000/authorized', scope=scope)

        # Open the authorization url
        print('Opening: ' + authorize_url)
        webbrowser.open(authorize_url)

        # Get code
        entered_code = str(input('Please enter code: '))
        # Exchange code for token:
        token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=entered_code)
        # Save it to file so we can use it until it expires.
        access_token_string = json.dumps(token_response)
        with open(access_token_file_name, 'w+') as f:
            json.dump(access_token_string, f)

    # Now we have a token_response dict either from file or from the
    # Strava API
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']

    print('access_token:',  access_token)
    print('refresh_token',  refresh_token )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get your access token to fetch data using Strava API")
    parser.add_argument('--client_id', required=True, help='The client id from your Strava App')
    parser.add_argument('--client_secret', required=True, help='The client secret from your Strava App')
    parser.add_argument('--output_file', default='access_token.json',
                    help='JSON file which will be stored the access token and credentials')
    parse_args(parser.parse_args())
