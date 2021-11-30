# iview-rss
To get the RSS feed for a show you can simply take the iView show id `https://iview.abc.net.au/show/<showid>` and use it in the app `https://iview-rss.maxstuff.net/rss/<showid>`

# Watchlist
Go to `https://iview.abc.net.au/watchlist` with devtools network open and search for `api.seesaw` then get the UID parameter of the request and use it for `https://iview-rss.maxstuff.net/watchlist/<uid>`

## Parameters (Standard for GET request)
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
|`include_extras`|`boolean`|`true`|This will either show or hide iView extra episodes|

To redeploy on server execute `sudo -u iview-rss bash && sudo systemctl restart iview-rss` then execute `cd ~/iview-rss && git pull && exit`
