import json
import webbrowser

from lib.consts import consts
from lib.trakt.trakt_objects import TraktRequest

class SecretsHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            with open(consts.get("secrets")) as f:
                cls._secrets = json.load(f)
        
        return cls._instance
    
    def get_secrets(self) -> dict:
        return self._secrets
    
    def update_secrets(self, secrets: dict):
        self._secrets.update(secrets)
        with open(consts.get("secrets"), 'w') as f:
            json.dump(self._secrets, f, indent=2)

class TokenHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.trakt_request = TraktRequest()
            cls.secrets_instance = SecretsHandler()
            cls.secrets = cls.secrets_instance.get_secrets()
        
        return cls._instance

    def get_token(self, refresh: bool=False):
        if not refresh:
            code = input(">> Enter the code: ")
            body = {
                "code": code,
                "grant_type": "authorization_code"
            }
        else:
            body = {
                "refresh_token": self.secrets.get("refresh_token"),
                "grant_type": "refresh_token"
            }

        if self.trakt_request.headers is None:
            self.trakt_request.set_default_headers(self.secrets.get("client_id"))
        
        body.update({
            "client_id": self.secrets.get("client_id"),
            "client_secret": self.secrets.get("client_secret"),
            "redirect_uri": self.secrets.get("redirect_uri"),
        })
        response = self.trakt_request.post(consts.get("trakt").get("token"), body)

        status_code = response.status_code
        data = response.json()

        if status_code == 401:
            print(data.get("error"))
            print(data.get("error_description"))
            if not refresh:
                exit()
            else:
                print("Authorize again..")
        else:
            self.secrets.update({
                "access_token": data.get("access_token"),
                "refresh_token": data.get("refresh_token"),
                "created_at": data.get("created_at"),
                "expires_in": data.get("expires_in")
            })
            self.secrets_instance.update_secrets(self.secrets)
        return (status_code, refresh)

class Authentictor:
    def __init__(self):
        self.response_type = "code"
        self.token_handler = TokenHandler()
        self.trakt_request = TraktRequest()
        self.secrets_instance = SecretsHandler()
        self.secrets = self.secrets_instance.get_secrets()
        
        self.auth_uri = None if self.secrets.get("client_id") is None\
            or self.secrets.get("redirect_uri") is None\
            or self.secrets.get("access_token") is None\
            else consts.get("trakt").get("auth")

    def authorize(self):
        if self.auth_uri is None:
            self.setup()
            webbrowser.open(self.auth_uri, new=1, autoraise=True)        
            stat_code, ref = self.token_handler.get_token(refresh=False)

            if stat_code == 401 and ref:
                self.auth_uri = None
                self.authorize()

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
        self.secrets_instance.update_secrets(self.secrets)
        self.set_auth_uri()

class Search:
    def __init__(self):
        self.trakt_request = TraktRequest()
        self.secrets_instance = SecretsHandler()
        self.secrets = self.secrets_instance.get_secrets()
    
    def query(self, qtype: str, q: str):
        uri = consts.get("trakt").get("search")\
            + f"{qtype}?"\
            + f"query={q}"
        
        self.trakt_request.set_default_headers(self.secrets.get("client_id"))
        self.trakt_request.set_headers({
            "X-Pagination-Page": '1',
            "X-Pagination-Limit": '10',
            "X-Pagination-Page-Count": '10',
            "X-Pagination-Item-Count": '100'
        })
        return self.trakt_request.get(uri)
