import typing
from abc import ABC

class TraktObject(ABC):
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

class TraktEpisode(TraktObject):
    def __init__(self, season_number: int, episode_number: int, show_title: str, watched_at: str):
        self.season_number = season_number
        self.episode_number = episode_number
        self.show_title = show_title
        self.watched_at = watched_at
    
    def json(self) -> dict:
        return {
            "watched_at": self.watched_at,
            "number": self.episode_number
        }

class TraktSeason(TraktObject):
    def __init__(self, season_number: int, show_title: str):
        self.season_number = season_number
        self.show_title = show_title
        self.episodes = typing.List[TraktEpisode]
    
    def add_episode(episode: TraktEpisode):
        self.episodes.append(episode)
    
    def json(self) -> dict:
        return {
            "number": self.season_number,
            "episodes": [episode.json for episode in self.episodes]
        }

class TraktShow(TraktObject):
    def __init__(self, show_title: str, release_year: int, ids: dict):
        self.show_title = show_title,
        self.release_year = release_year
        self.ids = ids
        self.seasons = typing.Dict[int, TraktSeason]
    
    def add_season(season: TraktSeason):
        self.seasons[season.season_number] = season
    
    def json(self) -> dict:
        return {
            "title": self.show_title,
            "year": self.release_year,
            "ids": self.ids,
            "seasons": [season.json for season in self.seasons]
        }
