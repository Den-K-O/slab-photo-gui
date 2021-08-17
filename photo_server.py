#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify

from waitress import serve

app = Flask(__name__)

@app.route('/bind/', methods=['GET']) # rfid,order_id
def check_binding():
    rfid = request.args.get('rfid')
    print (rfid)
    try:
        res=submit_rfid_location_to_db.card_order_binding(rfid)
        print (res)
        return jsonify({'result': "OK", 'rfid': rfid, 'order_id': res})
    except:
        return jsonify({'result': "ERROR", 'rfid': rfid, 'order_id': "not_found"})

serve(app, host='0.0.0.0', port=5000, threads=1)