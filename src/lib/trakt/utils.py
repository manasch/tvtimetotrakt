import json
import webbrowser

import questionary

from lib.consts import consts
from lib.trakt.trakt_objects import TraktRequest

class Authentictor:
    def __init__(self):
        self.response_type = "code"
        self.trakt_request = TraktRequest()
        with open(consts.get("secrets")) as f:
            self.secrets = json.load(f)
        
        self.auth_uri = None if self.secrets.get("client_id") is None\
            or self.secrets.get("redirect_uri") is None\
            or self.secrets.get("access_token") is None\
            else consts.get("trakt").get("auth")
    
    def authorize(self):
        if self.auth_uri is None:
            self.setup()
            webbrowser.open(self.auth_uri, new=1, autoraise=True)        
            self.get_access_token()
    
    def get_access_token(self):
        code = input(">> Enter the code: ")
        if self.trakt_request.headers is None:
            self.trakt_request.set_headers({
                "Content-type": "application/json",
                "trakt-api-key": self.secrets.get("client_id"),
                "trakt-api-version": 2
            })
        
        body = {
            "code": code,
            "client_id": self.secrets.get("client_id"),
            "client_secret": self.secrets.get("client_secret"),
            "redirect_uri": self.secrets.get("redirect_uri"),
            "grant_type": "authorization_code"
        }
        response = self.trakt_request.call(consts.get("trakt").get("token"), body)

        if response.get("error"):
            print(response.get("error"))
            print(response.get("error_description"))
            self.exchange_access_refresh()
        else:
            self.secrets.update({
                "access_token": response.get("access_token"),
                "refresh_token": response.get("refresh_token"),
                "created_at": response.get("created_at"),
                "expires_in": response.get("expires_in")
            })
            self.update_secrets()
            self.trakt_request.set_headers({
                "Authorization": f"Bearer {self.secrets.get('access_token')}"
            })
    
    def exchange_access_refresh(self):
        if self.trakt_request.headers is None:
            self.trakt_request.set_headers({
                "Content-type": "application/json",
                "trakt-api-key": self.secrets.get("client_id"),
                "trakt-api-version": 2
            })
        
        body = {
            "refresh_token": self.secrets.get("refresh_token"),
            "client_id": self.secrets.get("client_id"),
            "client_secret": self.secrets.get("client_secret"),
            "redirect_uri": self.secrets.get("redirect_uri"),
            "grant_type": "refresh_token"
        }
        response = self.trakt_request.call(consts.get("trakt").get("token"), body)

        if response.get("error"):
            print(response.get("error"))
            print(response.get("error_description"))
            print("Authorize again..")
            self.auth_uri = None
            self.authorize()
        else:
            self.secrets.update({
                "access_token": response.get("access_token"),
                "refresh_token": response.get("refresh_token"),
                "created_at": response.get("created_at"),
                "expires_in": response.get("expires_in")
            })
            self.update_secrets()
            self.trakt_request.set_headers({
                "Authorization": f"Bearer {self.secrets.get('access_token')}"
            })
    
    def update_secrets(self):
        with open(consts.get("secrets"), 'w') as f:
            json.dump(self.secrets, f, indent=2)
    
    def set_auth_uri(self):
        self.auth_uri = consts.get("trakt").get("auth")\
            + f"?response_type={self.response_type}"\
            + f"&client_id={self.secrets.get('client_id')}"\
            + f"&redirect_uri={self.secrets.get('redirect_uri')}"
    
    def setup(self):
        client_id = input(">> Enter the client id: ")
        client_secret = input(">> Enter the client secret: ")
        redirect_uri = input(">> Enter the redirect uri: ")
        
        self.secrets.update({
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        })
        self.update_secrets()
        self.set_auth_uri()

