from pathlib import Path

consts = {
    "trakt": {
        "base": "https://api.trakt.tv/",
        "auth": "https://api.trakt.tv/oauth/authorize/",
        "search": "https://api.trakt.tv/search/trakt/"
    },
    "tracked": {
        "episodes" : (Path.cwd().parent / "export" / "seen_episode.csv").resolve()
    }
}
