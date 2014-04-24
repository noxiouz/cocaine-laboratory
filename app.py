from flask import Flask
from flask import jsonify
from flask import request

from cocaine.services import Service

uatraits = Service("uatraits")

app = Flask(__name__)


@app.route('/')
def hello():
    ua = request.headers.get('User-Agent')
    res = uatraits.detect(ua).get()
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
