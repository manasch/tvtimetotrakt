import json
import webbrowser

import questionary

from lib.consts import consts

class Authentictor:
    def __init__(self):
        self.response_type = "code"
        self.uri = None
        with open(consts.get("secrets")) as f:
            self.secrets = json.load(f)
    
    def authorize(self):
        if self.uri is None:
            self.setup()
        print(self.uri)
        # webbrowser.open(self.uri, new=1, autoraise=True)
    
    def update_secrets(self):
        with open(consts.get("secrets"), 'w') as f:
            json.dump(self.secrets, f, indent=2)
    
    def setup(self):
        client_id = input(">> Enter the client id: ")
        redirect_uri = input(">> Enter the redirect uri: ")
        
        self.secrets.update({
            "client_id": client_id,
            "redirect_uri": redirect_uri
        })
        self.update_secrets()

        self.uri = consts.get("trakt").get("auth")\
            + f"?response_type={self.response_type}"\
            + f"&client_id={self.secrets.get('client_id')}"\
            + f"&redirect_uri={self.secrets.get('redirect_uri')}"
