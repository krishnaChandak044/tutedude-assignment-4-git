import hashlib
import json
import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
API_DATA = Path(__file__).with_name("items.json")
FORM = """<!doctype html><html lang='en'><meta charset='utf-8'><title>To-do</title>
<h1>To-do list</h1><form method='post' action='/submittodoitem'>
<label>Item ID <input name='itemId'></label><br>
<label>Item UUID <input name='itemUuid'></label><br>
<label>Item Hash <input name='itemHash'></label><br>
<label>Item Name <input name='itemName' required></label><br>
<label>Item Description <textarea name='itemDescription' required></textarea></label><br>
<button type='submit'>Save item</button></form></html>"""


def create_item(payload):
    name = str(payload.get("itemName", "")).strip()
    description = str(payload.get("itemDescription", "")).strip()
    if not name or not description:
        return None
    item = {
        "itemId": str(payload.get("itemId", "")).strip() or str(uuid.uuid4().int % 100000),
        "itemUuid": str(payload.get("itemUuid", "")).strip() or str(uuid.uuid4()),
        "itemHash": str(payload.get("itemHash", "")).strip()
        or hashlib.sha256(f"{name}\n{description}".encode("utf-8")).hexdigest(),
        "itemName": name,
        "itemDescription": description,
    }
    return item


@app.get("/")
def home():
    return render_template_string(FORM)


@app.get("/api")
def api_items():
    try:
        with API_DATA.open(encoding="utf-8") as source:
            return jsonify(json.load(source))
    except (OSError, json.JSONDecodeError):
        app.logger.exception("Could not read API JSON data")
        return jsonify(error="The API data file could not be read."), 500


@app.post("/submittodoitem")
def submit_todo_item():
    payload = request.get_json(silent=True) or request.form
    item = create_item(payload)
    if item is None:
        return jsonify(error="itemName and itemDescription are required"), 400

    mongo_uri = os.environ.get("MONGODB_URI", "").strip()
    if not mongo_uri:
        return jsonify(error="MONGODB_URI is not configured"), 503

    try:
        database = os.environ.get("MONGODB_DATABASE", "tutedude")
        collection = os.environ.get("MONGODB_COLLECTION", "todo_items")
        with MongoClient(mongo_uri, serverSelectionTimeoutMS=5000) as client:
            client.admin.command("ping")
            result = client[database][collection].insert_one(item)
        return jsonify(status="saved", item={**item, "_id": str(result.inserted_id)}), 201
    except PyMongoError:
        app.logger.exception("Could not save the to-do item to MongoDB")
        return jsonify(error="MongoDB is unavailable; verify the connection settings."), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
