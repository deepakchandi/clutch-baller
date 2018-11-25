from flask import Flask,render_template, request,jsonify,Response
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route("/compare", methods = ['GET'])
def compare():
    return render_template('compare.html')

# load the model
#model = pickle.load(open('linreg.p','rb'))

@app.route("/compare_stats", methods = ['GET'])
def compare_stats():
    df = pd.read_csv('stats_for_flask')
    data = list(zip(df))
    return jsonify(data)


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
