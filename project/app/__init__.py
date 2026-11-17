import json, os
from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "local-development-only"), MONGODB_URI=os.getenv("MONGODB_URI", ""), MONGODB_DATABASE=os.getenv("MONGODB_DATABASE", "tutedude"))
    if test_config: app.config.update(test_config)
    data_path = Path(app.root_path).parent / "data" / "items.json"
    @app.get("/")
    def index(): return render_template("index.html", error=None, values={})
    @app.get("/api")
    def api_items():
        try:
            with data_path.open(encoding="utf-8") as source: return jsonify(json.load(source))
        except (OSError, json.JSONDecodeError):
            app.logger.exception("Could not load API data")
            return jsonify({"error":"The API data file could not be read."}), 500
    @app.post("/submit")
    def submit():
        values={key:request.form.get(key, "").strip() for key in ("name","email","message")}
        if not all(values.values()): return render_template("index.html", error="Please complete every field.", values=values), 400
        if not app.config["MONGODB_URI"]: return render_template("index.html", error="Database is not configured. Set MONGODB_URI and try again.", values=values), 503
        try:
            with MongoClient(app.config["MONGODB_URI"], serverSelectionTimeoutMS=5000) as client:
                client.admin.command("ping")
                client[app.config["MONGODB_DATABASE"]]["submissions"].insert_one(values)
            return redirect(url_for("success"))
        except PyMongoError:
            app.logger.exception("MongoDB submission failed")
            return render_template("index.html", error="We could not save your submission. Check the database settings and try again.", values=values), 503
    @app.get("/success")
    def success(): return render_template("success.html")
    return app
