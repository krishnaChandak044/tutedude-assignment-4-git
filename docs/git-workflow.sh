#!/usr/bin/env bash
# Run in a fresh clone. The sandbox branch sequence demonstrates required operations.
set -euo pipefail
USER_BRANCH="KrishnaChandak044"
git checkout -b "$USER_BRANCH"
git add . && git commit -m 'Add Flask to-do project'
git checkout main && git merge --no-ff "$USER_BRANCH" -m 'Merge initial Flask project'
git checkout -b "${USER_BRANCH}_new"
printf '[{"id":1,"title":"Updated from _new","description":"conflict resolution branch"}]\n' > project/items.json
git add project/items.json && git commit -m 'Update API JSON on _new'
git checkout main
# Add main-side edit to ensure the merge generates a JSON conflict.
printf '[{"id":1,"title":"Updated from main","description":"conflicting update"}]\n' > project/items.json
git add project/items.json && git commit -m 'Update API JSON on main'
git merge "${USER_BRANCH}_new" || true
# Explicitly accept the _new branch version as required.
git checkout --theirs project/items.json
git add project/items.json && git commit -m 'Resolve JSON conflict using _new version'
git checkout -b master_1 main
# Features/fields are already represented by this project's form. Commit each addition independently.
git checkout --orphan _scratch_base >/dev/null 2>&1 || true
# Reset orphan attempt to restore branch context then use patch commits on master_1.
git checkout master_1
python3 - <<'PY'
p='project/app.py'; s=open(p).read(); s=s.replace('<label>Item ID <input name="itemId"></label><br>', ''); s=s.replace('<label>Item UUID <input name="itemUuid"></label><br>', ''); s=s.replace('<label>Item Hash <input name="itemHash"></label><br>', ''); open(p,'w').write(s)
PY
git add project/app.py && git commit -m 'Base to-do form fields'
python3 - <<'PY'
p='project/app.py'; s=open(p).read().replace('<label>Item Name <input', '<label>Item ID <input name="itemId"></label><br><label>Item Name <input'); open(p,'w').write(s)
PY
git add project/app.py && git commit -m 'Add Item ID field'
python3 - <<'PY'
p='project/app.py'; s=open(p).read().replace('<label>Item Name <input', '<label>Item UUID <input name="itemUuid"></label><br><label>Item Name <input'); open(p,'w').write(s)
PY
git add project/app.py && git commit -m 'Add Item UUID field'
python3 - <<'PY'
p='project/app.py'; s=open(p).read().replace('<label>Item Name <input', '<label>Item Hash <input name="itemHash"></label><br><label>Item Name <input'); open(p,'w').write(s)
PY
git add project/app.py && git commit -m 'Add Item Hash field'
git checkout main && git merge --no-ff master_1 -m 'Merge to-do form features'
# Locate the Item-ID-only commit; reset soft to it, then commit staged state as requested.
ITEM_ID_COMMIT=$(git log --format='%H %s' --grep='Add Item ID field' | head -1 | cut -d' ' -f1)
git reset --soft "$ITEM_ID_COMMIT"
git commit -m 'Recommit to-do fields through Item ID'
git checkout master_1
git rebase main master_1
