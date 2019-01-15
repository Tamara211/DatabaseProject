from myapp import app
from flask import request, jsonify




@app.route("/api/send", methods =['POST'])
def json_handle():
    json = request.get_json()
    for e in json:
        print("e : % s" % json[e])
    return "Got it"

@app.route("/")
@app.route("/index", methods =['GET', 'POST'])
def index():
    return "Hello World\n"


