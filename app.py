from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify({"Message": "Hello world! Version2"})

if __name__ == "__main__":
    app.run(debug=True)
