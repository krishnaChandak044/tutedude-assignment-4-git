# Assignment 4 — Git & GitHub

Repository: https://github.com/krishnaChandak044/tutedude-assignment-4-git

The project is a Flask to-do app with API JSON data, form fields for Item Name, Item Description, Item ID, Item UUID and Item Hash, and a POST `/submittodoitem` route. The POST endpoint validates required fields and inserts the item into MongoDB using `MONGODB_URI`; it returns a clear 503 response when MongoDB is not configured or unavailable. `.env.example` documents the configuration without credentials. `git log --all --graph` records the username branch, `_new` JSON conflict with `_new` accepted, `master_1` and `master_2`, independent ID/UUID/Hash commits, soft reset/recommit and a rebase of `master_1` onto main.

The existing SSH key authenticates as a different GitHub identity (`KrishnaChandak04`) than the active `gh` account (`krishnaChandak044`), so I did not change account security settings. The repo was pushed over the authenticated HTTPS session; public SSH clone is possible, but SSH push would require a key registered on the correct account.

Run: `pip install -r project/requirements.txt`, set `MONGODB_URI` (and optional database/collection names), then `cd project && python app.py`. The deployed MongoDB integration was not exercised because no MongoDB service URI was provided.
