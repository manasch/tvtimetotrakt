import logging

from lib.tvtime2trakt import TVTime2Trakt

logging.basicConfig(filename="logs.log", level=logging.DEBUG)

def main():
    tvtime2trakt = TVTime2Trakt()
    tvtime2trakt.run()

if __name__ == "__main__":
    main()
