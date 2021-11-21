import os
from honeybadger import honeybadger

if 'HONEY_BADGER_KEY_IVIEW_RSS_MAXSTUFF_NET' in os.environ:
    honeybadger.configure(api_key=os.environ['HONEY_BADGER_KEY_IVIEW_RSS_MAXSTUFF_NET'])
else:
    print("\n\n\nWARNING: HONEY_BADGER_KEY_IVIEW_RSS_MAXSTUFF_NET NOT SET ERRORS WILL NOT BE REPORTED!\n\n\n")

import flask
import requests
import json
import datetime
import time
from feedgen.feed import FeedGenerator

app = flask.Flask(__name__)

@app.route("/")
def index():
    return 'iView RSS'

@app.route("/rss/<show>")
def rss_show(show):
    request_result = requests.get(
        "https://api.iview.abc.net.au/v2/show/"+show
    )
    if request_result.status_code == 200:
        request_result_content = request_result.content.decode()
        show_info = json.loads(request_result_content)
        fg = FeedGenerator()
        fg.id('https://iview.abc.net.au/show/'+show)
        fg.title(show_info['title'])
        fg.link(href='https://iview.abc.net.au/show/'+show, rel="alternate")
        fg.language('en')
        fg.author({'name':'Max','uri':'https://maxstuff.net'})
        fg.description(show_info['description'])
        if show_info['type'] == 'series':
            for series in show_info['_embedded']['seriesList']:
                current_series = json.loads(
                    requests.get(
                        "https://api.iview.abc.net.au/v2"+series['_links']['deeplink']['href']
                    ).content.decode()
                )
                for episode in current_series['_embedded']['selectedSeries']['_embedded']['videoEpisodes']:
                    fe = fg.add_entry()
                    fe.id("https://iview.abc.net.au"+episode['_links']['self']['href'])
                    series_text=""
                    if current_series['_links']['selectedSeries']['id'] != '0':
                        series_text = "S"+current_series['_links']['selectedSeries']['id']+" "
                    fe.title(f'{series_text}{episode["title"]}')
                    epiry_date = datetime.datetime.strptime(episode['expireDate'],"%Y-%m-%d %H:%M:%S").strftime("%I:%M%p %d/%m/%Y")
                    fe.description(f"Expires {epiry_date}\n{episode['description']}")
                    fe.link(href=episode['shareUrl'])
                    fe.published(datetime.datetime.strptime(episode['pubDate'],"%Y-%m-%d %H:%M:%S").astimezone())
            resp = flask.Response(fg.rss_str(pretty=True))
            resp.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
            return resp
        else:
            honeybadger.notify(f"{show_info['type']} show type is not recognised!", context={"show_id": show})
            return "501", 501
    elif request_result.status_code == 404:
        return "404", 404
    else:
        honeybadger.notify(f"{request_result.status_code} error code is not recognised!", context={"show_id": show})
        return "501", 501

LAST_GIT_PULL = 0

@app.route("/deploy_hook")
def deploy_hook():
    global LAST_GIT_PULL
    if LAST_GIT_PULL+10 > int(time.time):
        os.system("git pull")
        return datetime.datetime.now().ctime()
    return "429", 429
