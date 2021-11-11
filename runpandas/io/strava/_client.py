"""
Tool to get/refresh Strava Token.
"""
from stravalib.client import Client
import os
import json
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
from urllib.parse import urlsplit, parse_qs


def coalesce(iterable):
    return next((el for el in iterable if el is not None), None)


class HTTPResponder(HTTPServer):
    allow_reuse_address = True
    timeout = 60

    def handle_timeout(self):
        self.server_close()


class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle OAuth redirects
    """

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if "code" in self.path:
            self.auth_code = parse_qs(urlsplit(self.path).query)["code"]
            self.wfile.write(
                bytes(
                    "<html><h1>You may now close this window."
                    + "</h1></html>",
                    "utf-8",
                )
            )
            self.server.access_token = self.auth_code

    # Disable logging from the HTTP Server
    def log_message(self, format, *args):
        return


class StravaClient(Client):
    def __init__(
        self,
        *args,
        token_file=None,
        refresh_token=None,
        client_secret=None,
        client_id=None,
        **kwargs
    ):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.token_file = coalesce(
            (token_file, os.getenv("STRAVA_TOKEN_FILE", None))
        )
        self.client_secret = coalesce(
            (client_secret, os.getenv("STRAVA_CLIENT_SECRET", None))
        )
        self.client_id = coalesce(
            (client_id, os.getenv("STRAVA_CLIENT_ID", None))
        )

        if self.token_file is not None:
            self.get_token_from_file()

        if refresh_token is not None:
            self.refresh_token = refresh_token

    def set_token_from_dict(self, token):
        self.access_token = token["access_token"]
        self.refresh_token = token["refresh_token"]
        self.token_expires_at = token["expires_at"]

    def get_token_from_file(self):
        if self.token_file is not None:
            with open(self.token_file, "r") as f:
                token = json.load(f)
        if token is not None:
            if type(token) == str:
                token = json.loads(token)
            self.set_token_from_dict(token)

    def save_token_to_file(self, token):
        if self.token_file is None:
            return None
        with open(self.token_file, "w") as f:
            f.write(json.dumps(token))

    def refresh(self):
        if time.time() > self.token_expires_at:
            token = self.refresh_access_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=self.refresh_token,
            )
            if self.token_file is not None:
                with open(self.token_file, "w") as f:
                    f.write(json.dumps(token))

    def authenticate_web(self):
        scope = [
            "read",
            "read_all",
            "profile:read_all",
            "activity:read",
            "activity:read_all",
        ]
        authorize_url = self.authorization_url(
            client_id=self.client_id,
            redirect_uri="http://localhost:5000/authorized",
            scope=scope,
        )
        webbrowser.open(authorize_url)
        httpServer = HTTPResponder(
            ("localhost", 5000),
            lambda request, address, server: HTTPServerHandler(
                request, address, server
            ),
        )
        httpServer.handle_request()

        # Exchange code for token:
        token_response = self.exchange_code_for_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=httpServer.access_token,
        )
        # Save it to file so we can use it until it expires.
        access_token_string = json.dumps(token_response)
        if self.token_file is not None:
            with open(self.token_file, "w+") as f:
                json.dump(access_token_string, f)
