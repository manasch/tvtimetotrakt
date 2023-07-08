from pathlib import Path

consts = {
    "trakt": {
        "base": "https://api.trakt.tv/",
        "auth": "https://api.trakt.tv/oauth/authorize/",
        "search": "https://api.trakt.tv/search/",
        "token": "https://api.trakt.tv/oauth/token/",
        "history": "https://api.trakt.tv/sync/history"
    },
    "tracked": {
        "episodes" : (Path.cwd().parent / "export" / "seen_episode.csv").resolve()
    },
    "secrets_format": {
        "client_id": None,
        "client_secret": None,
        "redirect_uri": None,
        "access_token": None,
        "refresh_token": None
    },
    "secrets": (Path.cwd() / "lib" / "secrets.json").resolve(),
    "payload": (Path.cwd() / "payload.json").resolve(),
    "no_match": (Path.cwd() / "no_match.json").resolve(),
    "timezone": (Path.cwd() / "lib" / "timezone").resolve()
}
