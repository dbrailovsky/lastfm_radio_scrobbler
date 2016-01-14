# Lastfm Radio Scrobbler
Scrobble shoutcast radio 

## Configuration file
Path to config ~/.lastfm_scrobbler/lastfm.json
It contains something like this:
```json
{
	"api_key" : apikey,
	"user_name": username,
	"app_name": app_name,
	"shared_secret": api_secret,
	"password": password_md5_hash
}
```

## Run
python lastfm_radio_scrobble.py name=<radio_url>
Press button Scrobble
