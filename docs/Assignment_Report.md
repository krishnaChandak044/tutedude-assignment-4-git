# Assignment 4 — Git & GitHub, Flask and MongoDB

**Repository:** https://github.com/krishnaChandak044/tutedude-assignment-4-git

## Work completed

The repository contains the Flask to-do interface and `POST /submittodoitem` endpoint. The handler accepts form or JSON input, validates Item Name and Item Description, supplies Item ID, UUID and SHA-256 hash values when omitted, and inserts records into a MongoDB collection. The `_new` branch JSON conflict was resolved by retaining `_new`'s version. The Git history includes username, `master_1`, and `master_2` branches; separate Item ID, UUID, and Hash commits; soft-reset/recommit; and rebasing `master_1` onto main. Branch history is included in `evidence/git-history.txt`.

## Run and configure

Install `project/requirements.txt`, configure `MONGODB_URI` from a MongoDB deployment, then run `python app.py` from `project/`. `.env.example` contains placeholders only. MongoDB connectivity was not exercised because a database URI/service was not available. The repository was pushed using the already authenticated HTTPS session because the local SSH key is associated with a different GitHub identity; no account security setting was changed.
