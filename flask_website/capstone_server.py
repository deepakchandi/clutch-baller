from flask import Flask,render_template, request,jsonify,Response
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    return '<h1> Hello World </h1><p>My name is Elliott</p>'






if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
