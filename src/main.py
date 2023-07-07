import json
import logging

from lib.tvtime.tvtime_parser import TVTimeParser
from lib.consts import consts
from lib.trakt.utils import Authentictor, Search

logging.basicConfig(filename="logs.log", level=logging.DEBUG)
# parser = TVTimeParser(consts.get("tracked").get("episodes"))
# parser.parse()

authenticator = Authentictor()
authenticator.authorize()
