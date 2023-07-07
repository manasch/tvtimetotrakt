import json

from lib.tvtime.tvtime_parser import TVTimeParser
from lib.consts import consts
from lib.trakt.utils import Authentictor

class TVTime2Trakt:
    def __init__(self):
        self.authenticator = Authentictor()
        self.parser = TVTimeParser(consts.get("tracked").get("episodes"))

    def run(self):
        self.authenticator.authorize()
        self.parser.parse()
