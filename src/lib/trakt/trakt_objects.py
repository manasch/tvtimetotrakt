import typing
from abc import ABC

import requests

class TraktObject(ABC):
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

class TraktEpisode(TraktObject):
    def __init__(self, season_number: int, episode_number: int, show_title: str, watched_at: str):
        self.season_number = season_number
        self.episode_number = episode_number
        self.show_title = show_title
        self.watched_at = watched_at
    
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.S{self.season_number}.E{self.episode_number}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.S{self.season_number}.E{self.episode_number}>"
    
    def json(self) -> dict:
        return {
            "watched_at": self.watched_at,
            "number": self.episode_number
        }

class TraktSeason(TraktObject):
    def __init__(self, season_number: str, show_title: str):
        self.season_number = season_number
        self.show_title = show_title
        self.episodes: typing.List[TraktEpisode] = list()
    
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.{self.season_number}<{len(self.episodes)}>>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.{self.season_number}<{len(self.episodes)}>>"
    
    def add_episode(self, episode: TraktEpisode):
        self.episodes.append(episode)
    
    def json(self) -> dict:
        return {
            "number": self.season_number,
            "episodes": [episode.json() for episode in self.episodes]
        }

class TraktShow(TraktObject):
    def __init__(self, show_title: str, release_year: int, ids: dict):
        self.show_title: str = show_title
        self.release_year = release_year
        self.ids = ids
        self.seasons: typing.Dict[str, TraktSeason] = dict()
    
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.{self.release_year}<{len(self.seasons)}>>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self.show_title}.{self.release_year}<{len(self.seasons)}>>"
    
    def add_episode(self, episode: TraktEpisode):
        if not self.seasons.get(episode.season_number):
            self.seasons[episode.season_number] = TraktSeason(episode.season_number, self.show_title)
        
        self.seasons[episode.season_number].add_episode(episode)
    
    def json(self) -> dict:
        return {
            "title": self.show_title,
            "year": self.release_year,
            "ids": self.ids,
            "seasons": [season.json() for season in self.seasons.values()]
        }

class TraktRequest(TraktObject):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.session = requests.session()
            cls.headers = dict()
            cls.cookies = None
        
        return cls._instance
    
    def set_headers(self, headers: dict):
        self.headers.update(headers)
    
    def set_default_headers(self, client_id: str):
        self.headers = {
            "Content-type": "application/json",
            "trakt-api-key": client_id,
            "trakt-api-version": '2'
        }
    
    def set_cookies(self, cookies: dict):
        self.cookies.update(cookies)
    
    def post(self, uri: str, body: dict):
        res = self.session.post(uri, headers=self.headers, json=body)
        return res
    
    def get(self, uri: str, body: dict=None):
        res = self.session.get(uri, headers=self.headers, json=body)
        return res
