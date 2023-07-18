# TVTime to Trakt

## What does it do?

- Parses the TVTime data, along with the date and time for each episode and creates a payload.
- This payload is then sent to trakt's API to update your watch history. `src/payload.json`.
- Shows which couldn't be found during the search are stored in `src/no_match.json`. (Adding this to history hasn't been automated yet.)

> This only works for TV Shows on TvTime.

---

## Setup

- Trakt api app. (A new one can be created [here](https://trakt.tv/oauth/applications))
    - Keep the client id, secret and redirect uri copied somewhere.
- TVTime personal data. This can be obtained by sending an email of [this format](https://www.datarequests.org/blog/sample-letter-gdpr-access-request/) to [TVTime support](support@tvtime.com).
    - This could take up to a week to be sent depending on the size.
    - Create a new folder called `export` in the root directory.
    - Extract the contents from the zip file and place them in the `export` directory.
    - `seen_episode.csv` is the only file that is used.
- Python 3.8 or above.
- `pip install -r requirements.txt`
- Navigate to the src folder in the terminal and run
```bash
python main.py
```
or
```bash
python3 main.py
```
- Follow the steps displayed in the terminal.

> Make sure to enter the correct timezone for conversion as trakt processes data in UTC.

---

### Notes

- This processes the entire data first before sending any updates to the api.
- Opens one session and only makes requests to the api during search when coming across an episode from a show for the first time.
- The order at which the episodes were watched doesn't matter.
- Once the data has been processed, the payload that will be sent to trakt api is stored in `src/payload.json` and the items which couldn't be matched are stored in `src/no_match.json`.
- The handling of unmatched items hasn't been implemented yet.
- Makes only one post request to trakt to update the history.
- The episodes are processed and stored in a tree-like structure making it easy to handle.