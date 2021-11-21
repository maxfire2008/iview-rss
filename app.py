from honeybadger import honeybadger
honeybadger.configure(api_key='hbp_lV19LQk4cRD0WUcO7cZ1sW2iS3hk8g1ZNec6')

import flask
import requests
import json

#honeybadger.notify(exc, context={'foo': 'bar'})

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
        pass
    else:
        honeybadger.notify(f"{show_info['type']} is not recognised!", context=show)
    return show

