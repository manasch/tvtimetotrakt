import atexit
import csv
import json
import typing
from pathlib import Path

from lib.consts import consts
from lib.trakt.trakt_objects import TraktEpisode, TraktSeason, TraktShow
from lib.trakt.utils import Search

class TVTimeParser():
    def __init__(self, seen_episodes_path: Path):
        self.seen_episode_file_pointer = open(seen_episodes_path, encoding="utf-8")
        self.search = Search()
        self.reader = csv.DictReader(self.seen_episode_file_pointer)
        self.shows: typing.Dict[str, TraktShow] = dict()
        self.no_match: typing.Dict[str, TraktShow] = dict()
        atexit.register(self.close_file)
    
    def parse(self):
        for row in self.reader:
            episode = TraktEpisode(row["episode_season_number"], row["episode_number"], row["tv_show_name"], row["updated_at"])
            print(str(episode))

            if not self.shows.get(episode.show_title):
                res = self.search.query("show", episode.show_title)
                if res.status_code == 200 and res.text != "[]":
                    best_match = res.json()[0]
                    new_entry = TraktShow(
                        best_match.get("show").get("title"),
                        best_match.get("show").get("year"),
                        best_match.get("show").get("ids")
                    )
                    self.shows[episode.show_title] = new_entry
                elif res.status_code == 200 and res.text == "[]":
                    if not self.no_match.get(episode.show_title):
                        self.no_match[episode.show_title] = TraktShow(
                            episode.show_title,
                            1970,
                            {}
                        )
                    self.no_match.get(episode.show_title).add_episode(episode)
                    continue
                else:
                    raise Exception("HTTP Error")
            
            show = self.shows.get(episode.show_title)
            show.add_episode(episode)
                                                
        with open(consts.get("payload"), "w", encoding="utf-8") as f,\
            open(consts.get("no_match"), "w", encoding="utf-8") as g:
            payload = {
                "shows": list()
            }
            dump = {
                "shows": list()
            }

            for _, tvshow in self.shows.items():
                payload.get("shows").append(tvshow.json())
            
            for _, tvshow in self.no_match.items():
                dump.get("shows").append(tvshow.json())

            json.dump(payload, f, indent=2)
            json.dump(dump, g, indent=2)
    
    def close_file(self):
        self.seen_episode_file_pointer.close()
