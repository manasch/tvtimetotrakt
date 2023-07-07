from lib.tvtime.tvtime_parser import TVTimeParser
from lib.consts import consts

parser = TVTimeParser(consts.get("tracked").get("episodes"))

parser.parse()
