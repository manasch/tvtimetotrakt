from pathlib import Path

from lib.tvtime.tvtime_parser import TVTimeParser

seen_path = (Path.cwd().parent / "export" / "seen_episode.csv").resolve()
parser = TVTimeParser(seen_path)

parser.parse()
