# Assignment 4 — Git & GitHub

Repository: https://github.com/krishnaChandak044/tutedude-assignment-4-git

The project is a Flask to-do app with an API JSON file, form fields for Item Name, Item Description, Item ID, Item UUID and Item Hash, and a POST `/submittodoitem` route. `git log --all --graph` in the repository records the username branch, `_new` JSON conflict with `_new` accepted, `master_1` and `master_2`, independent ID/UUID/Hash commits, soft reset/recommit and a rebase of `master_1` onto main.

The existing SSH key authenticates as a different GitHub identity (`KrishnaChandak04`) than the active `gh` account (`krishnaChandak044`), so I did not change account security settings. The repo was pushed over the authenticated HTTPS session; public SSH clone is possible, but SSH push would require a key registered on the correct account.

Run: `pip install -r project/requirements.txt && cd project && python app.py`.
