import requests
import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape
import pickle
import inputScript   #inputScript file - to analyze the URL


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "z9W233d1IzKQln7pNbPLagwK1M9sChdB893Z_zWTXeGN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def predict():
    return render_template("index.html")

#  fetches given URL and passes to inputScript

def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)

    return check_predic


@app.route('/predict', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)

    payload_scoring = {"input_data": [{"field": 'url', "values": y_predict([np.array(list(data.values()))])}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/29c08d03-9cdb-4113-86fa-67750be82b72/predictions?version=2022-10-18', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})

    result = response_scoring.json()

    predic = result[0]

    if(predic==1):
        pred = "You are safe!! This is a Legimate Website :)"
    else:
        pred = "You are in a wrong site. Be Cautious :("

    return render_template("index.html", pred_text = '{}'.format(pred))

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)