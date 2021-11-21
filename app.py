import flask
import requests
import json

app = flask.Flask(__name__)

@app.route("/")
def index():
    return 'iView RSS'

@app.route("/rss/<show>")
def rss_show(show):
    show_info = json.loads(
        requests.get(
            "https://api.iview.abc.net.au/v2/show/"+show
        ).content.decode()
    )
    if show_info['type'] == 'series':
        
    return show

