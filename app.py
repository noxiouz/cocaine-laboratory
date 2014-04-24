import json
import time
import uuid

from flask import Flask, abort
from flask import request
from flask import render_template

from cocaine.services import Service
from cocaine.logging import Logger

logger = Logger()

storage = Service("storage")
converter = Service("converter")

app = Flask(__name__)

META_NAMESPACE = "Description"
META_TAG = ["META"]

DATA_NAMESPACE = "Data"
DATA_TAG = ["DATA"]

TEMP_DATA_NAMESPACE = "TempData"
TEMP_DATA_TAG = []

FILTERS = ["KelvinFilter",
           "NashvilleFilter",
           "ToasterFilter",
           "GothamFilter",
           "LomoFilter"]


@app.route('/upload', methods=['POST'])
def upload():
    uploadedFile = request.files['uploadFile']
    with uploadedFile.stream as f:
        data = f.read()
    logger.info("Incoming image size %d" % len(data))
    # ====
    futures = list()
    for fls in FILTERS:
        logger.info("Apply filter %s" % fls)
        f = converter.enqueue(fls, data)
        futures.append(f)

    handled_images = list()
    for future in futures:
        logger.info("Get result")
        handled_images.append(future.get(timeout=2))

    # ====
    res = list()
    for image in handled_images:
        uid = uuid.uuid4().hex
        try:
            storage.write(TEMP_DATA_NAMESPACE, uid, image, TEMP_DATA_TAG)
        except Exception:
            pass  # ChokeEvent
        res.append(uid)
    logger.info("Send results %d" % len(res))
    return render_template('car.html', photos=res)


@app.route('/apply/<uid>', methods=['GET'])
def apply(uid):
    # get temp file
    data = storage.read(TEMP_DATA_NAMESPACE, uid).get()
    try:
        storage.write(DATA_NAMESPACE, uid, data, DATA_TAG).get()
    except Exception as err:
        print err

    meta = {"src": "/getimage/%s" % uid, "timestamp": int(time.time())}
    try:
        storage.write(META_NAMESPACE, uid,
                      json.dumps(meta), META_TAG).get()
    except Exception as err:
        print err
    return "Done"


@app.route('/')
def main():
    meta = list()
    keys = storage.find(META_NAMESPACE, META_TAG).get()
    for key in keys:
        meta.append(json.loads(storage.read(META_NAMESPACE, key).get()))

    meta = sorted(meta, key=lambda x: x['timestamp'], reverse=True)[:20]
    return render_template('index.html', photos=meta)


@app.route('/gettempimage/<uid>')
def gettempimage(uid):
    try:
        blob = storage.read(TEMP_DATA_NAMESPACE, uid).get()
    except Exception:
        abort(404)
    else:
        return blob


@app.route('/getimage/<uid>')
def getimage(uid):
    try:
        blob = storage.read(DATA_NAMESPACE, uid).get()
    except Exception:
        abort(404)
    else:
        return blob


@app.route('/ping')
def ping():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
