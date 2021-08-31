#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, render_template
import slab_photo_client_awaitable
import asyncio


from waitress import serve
i=0 
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():   
    global i
    i+=1
    if request.method == 'GET':
        row={
        "wood" : "горіх",
        "thickness": 60,
        }
        asyncio.run(slab_photo_client_awaitable.main(row)) 
        return f"OK, {i}"
    
    return render_template("index.html")

serve(app, host='0.0.0.0', port=5000, threads=1)