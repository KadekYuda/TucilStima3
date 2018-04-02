from flask import *
import sys
import json
app = Flask(__name__)

@app.route("/")
def launch():
    return render_template("index.html")

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.get_json()
    # cara akses data json
    # jsdata['coordinates'][idx]['lat'] nerima latitude
    # jsdata['coordinates'][idx]['lng'] nerima longitude
    return json.dumps(jsdata)[0];

if __name__ == "__main__":
    app.run()
