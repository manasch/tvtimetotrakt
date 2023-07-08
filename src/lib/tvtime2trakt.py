import json

from lib.tvtime.tvtime_parser import TVTimeParser
from lib.consts import consts
from lib.trakt.utils import Authentictor, UpdateHistory

class TVTime2Trakt:
    def __init__(self):
        self.authenticator = Authentictor()
        self.parser = TVTimeParser(consts.get("tracked").get("episodes"))
        self.updater = UpdateHistory()

    def run(self):
        self.authenticator.authorize()
        self.parser.parse()
        print("A summary of the parsed content can be found in:", consts.get("payload"))

        update = input("Go ahead with updating trakt history [y/n]: ").lower()
        if update == 'y':
            response = self.updater.update()
            print(json.dumps(response.json(), indent=2))
        elif update == 'n':
            pass
        else:
            print("Invalid input..")
        print("Exiting...")
