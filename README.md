# youtube-playlist-sync

modify sample.config.json -> config.json
change json values

Key | Value
--- | ---
api-key | api key creds from google api console
playlist-id | youtube playlist id (usually at the end of the url)

```
python playlist.py
```

creates folder for storage

keeps a log of video id's to prevent dup downloads
