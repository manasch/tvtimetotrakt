from pathlib import Path

consts = {
    "trakt": {
        "base": "https://api.trakt.tv/",
        "auth": "https://api.trakt.tv/oauth/authorize/",
        "search": "https://api.trakt.tv/search/trakt/",
        "token": "https://api.trakt.tv/oauth/token/"
    },
    "tracked": {
        "episodes" : (Path.cwd().parent / "export" / "seen_episode.csv").resolve()
    },
    "secrets": (Path.cwd() / "lib" / "secrets.json").resolve()
}
