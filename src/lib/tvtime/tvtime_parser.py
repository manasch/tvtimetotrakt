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
        self.no_match: typing.List[TraktEpisode] = list()
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
                    self.no_match.append(episode)
                    continue
                else:
                    raise Exception("HTTP Error")
            
            show = self.shows.get(episode.show_title)
            show.add_episode(episode)
        
        with open(consts.get("no_match"), "w", encoding="utf-8") as f:
            dump = {
                "shows": list()
            }
            for episode in self.no_match:
                dump.get("shows").append({
                    "Title": episode.show_title,
                    "Season": episode.season_number,
                    "Episode": episode.episode_number,
                    "Watched At": episode.watched_at,
                })

            json.dump(dump, f, indent=2)
                                        
        with open(consts.get("payload"), "w", encoding="utf-8") as f:
            payload = {
                "shows": list()
            }
            for _, tvshow in self.shows.items():
                payload.get("shows").append(tvshow.json())
            
            json.dump(payload, f, indent=2)
    
    def close_file(self):
        self.seen_episode_file_pointer.close()
