import atexit
import csv
import datetime
import json
import typing
from pathlib import Path

from lib.consts import consts
from lib.trakt.trakt_objects import TraktEpisode, TraktSeason, TraktShow
from lib.trakt.utils import Search

class Timezone:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            with open(consts.get("timezone")) as f:
                cls.timezonestring = f.readline()
            cls.sign = cls.timezonestring[3]
            cls.hours = int(cls.timezonestring[4:6])
            cls.mins = int(cls.timezonestring[7:9])
            cls.total_offset_mins = cls.hours * 60 + cls.mins
            cls.offset_mins = cls.total_offset_mins if cls.sign == '+' else -cls.total_offset_mins
            cls.offset = datetime.timedelta(minutes=cls.offset_mins)
        
        return cls._instance

class TVTimeParser:
    def __init__(self, seen_episodes_path: Path):
        self.seen_episode_file_pointer = open(seen_episodes_path, encoding="utf-8")
        self.search = Search()
        self.reader = csv.DictReader(self.seen_episode_file_pointer)
        self.shows: typing.Dict[str, TraktShow] = dict()
        self.no_match: typing.Dict[str, TraktShow] = dict()
        self.timezone = Timezone()
        atexit.register(self.close_file)
    
    def convert_to_utc(self, date_time: str) -> str:
        input_time = datetime.datetime.strptime(date_time, r"%Y-%m-%d %H:%M:%S")
        utc_time = input_time - self.timezone.offset
        return utc_time.strftime(r"%Y-%m-%d %H:%M:%S")
    
    def parse(self):
        for row in self.reader:
            episode = TraktEpisode(
                row["episode_season_number"],
                row["episode_number"],
                row["tv_show_name"],
                self.convert_to_utc(row["updated_at"])
            )
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
        
        if len(self.no_match) > 0:
            print("Trakt couldn't find the information on these shows:", consts.get("no_match"))
            print("Handling this has not yet been implemented, add these shows manually or change their names in", consts.get("tracked").get("episodes"))
    
    def close_file(self):
        self.seen_episode_file_pointer.close()
