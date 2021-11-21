import flask
import requests
import re

app = flask.Flask(__name__)
#window.__INITIAL_STATE__ {0,}= {0,}("|').{0,}("|');
def getShowEpisodes():
    fx=re.search("window.__INITIAL_STATE__ {0,}= {0,}(\"|').{0,}(\"|');",r.content.decode())[0]
    abc=json.loads(fx[28:-2].replace('\\"','"').replace("\\'","'"))

@app.route("/")
def index():
    return 'iView RSS'

@app.route("/rss/<show>")
def rss_show(show):
    return show

