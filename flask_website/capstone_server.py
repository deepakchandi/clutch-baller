from flask import Flask,render_template, request,jsonify,Response
import pickle
import pandas as pd
import numpy as np
from code_for_flask import player_stat


app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route("/compare", methods = ['GET'])
def compare():
    return render_template('compare.html')

# load the model
#comp = pickle.load(open('comparison.p','rb'))



@app.route("/stat", methods = ['GET'])
def stat():
    req = request.get_json()
    print(req)
    name1, name2 = req['player'], req['player']
    stats = list(comp(name1, name2))
    return jsonify({"stats": stats})


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
