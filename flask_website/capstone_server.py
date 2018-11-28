from flask import Flask,render_template, request,jsonify,Response, send_from_directory
import pickle
import pandas as pd
import numpy as np
from code_for_flask import player_stat
import io
import json


app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route("/compare", methods = ['GET'])
def compare():
    return render_template('compare.html')

# load the model
comp = pickle.load(open('comparison.p','rb'))

#need to make a route for this by making a json page
@app.route("/inference", methods = ['POST'])
def inference():
    req = request.get_json()
    print(req)
    df = pd.read_csv('stats_for_flask')
    name1, name2 = req['Player1'], req['Player2']
    stats = comp(name1, name2, df)
    return  stats.to_json()


# @app.route('/jqgrid/<path:path>')
# def send_js(path):
#     return send_from_directory('templates/jqgrid', path)



if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
