import atexit
import csv
import json
import typing
from pathlib import Path

from lib.trakt.trakt_objects import TraktEpisode, TraktSeason, TraktShow

class TVTimeParser():
    def __init__(self, seen_episodes_path: Path):
        self.seen_episode_file_pointer = open(seen_episodes_path)
        self.reader = csv.DictReader(self.seen_episode_file_pointer)
        self.shows: typing.Set[TraktShow] = set()
        self.show_map: typing.Dict[str, TraktShow] = dict()
        atexit.register(self.close_file)
    
    def parse(self):
        for row in self.reader:
            episode = TraktEpisode(row["episode_season_number"], row["episode_number"], row["tv_show_name"], row["updated_at"])

            if not self.show_map.get(episode.show_title):
                pass
            
            show = self.show_map.get(episode.show_title)
            show.add_episode(episode)
    
    def close_file(self):
        self.seen_episode_file_pointer.close()
