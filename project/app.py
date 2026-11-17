from flask import Flask, jsonify, request
import json, uuid, hashlib
app=Flask(__name__)
@app.get('/api')
def api():
    with open('items.json', encoding='utf-8') as f: return jsonify(json.load(f))
@app.get('/')
def home():
    return '''<!doctype html><title>To-do</title><h1>To-do list</h1><form method="post" action="/submittodoitem"><label>Item Name <input name="itemName" required></label><br><label>Item Description <textarea name="itemDescription" required></textarea></label><button>Save</button></form>'''
@app.post('/submittodoitem')
def submit():
    values={k:request.form.get(k,'').strip() for k in ['itemId','itemUuid','itemHash','itemName','itemDescription']}
    values['itemId']=values['itemId'] or str(uuid.uuid4().int % 100000)
    values['itemUuid']=values['itemUuid'] or str(uuid.uuid4())
    values['itemHash']=values['itemHash'] or hashlib.sha256((values['itemName']+values['itemDescription']).encode()).hexdigest()
    if not values['itemName'] or not values['itemDescription']: return jsonify(error='itemName and itemDescription are required'),400
    with open('items.json',encoding='utf-8') as f: items=json.load(f)
    items.append(values)
    with open('items.json','w',encoding='utf-8') as f: json.dump(items,f,indent=2)
    return jsonify(status='saved',item=values),201
if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
