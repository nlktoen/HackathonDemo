# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 20:11:27 2020

@author: ADMIN
"""

"""
@author: nlktoen
"""

from flask import Flask, request, url_for, redirect, render_template, jsonify, send_from_directory
import flask
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as graph

app = flask.Flask(__name__, static_url_path='')
model_cancer = pickle.load(open("model-cancer.pkl", "rb"))
model_biopsy = pickle.load(open("model-biopsy.pkl", "rb"))
model_cin = pickle.load(open("model-CIN.pkl", "rb"))
model_citology = pickle.load(open("model-citology.pkl", "rb"))
model_hinselmann = pickle.load(open("model-hinselmann.pkl", "rb"))
model_hpv = pickle.load(open("model-hpv.pkl", "rb"))
model_schiller = pickle.load(open("model-schiller.pkl", "rb"))
scaler_biopsy= pickle.load(open("scaler-biopsy","rb"))
scaler_cancer= pickle.load(open("scaler-cancer","rb"))
scaler_cin= pickle.load(open("scaler-CIN","rb"))
scaler_citology= pickle.load(open("scaler-citology","rb"))
scaler_hinselmann= pickle.load(open("scaler-hinselmann","rb"))
scaler_hpv= pickle.load(open("scaler-hpv","rb"))
scaler_schiller= pickle.load(open("scaler-schiller","rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/bootstrap/<path:path>')
def send_js(path):
    return send_from_directory('bootstrap', path)

@app.route('/predict',methods=['POST'])



#1
def dx_cancer():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final])
    scaler=[scaler_cancer,scaler_biopsy,scaler_cin ,scaler_citology,scaler_hinselmann,scaler_hpv,scaler_schiller]
    data_unseen_scaled=[]
    for i in range(7):
        data_unseen_scaled.append(scaler[i].transform(data_unseen))
    con_level = {}
    test_result = {}
    test_list = [model_cancer,model_biopsy,model_cin ,model_citology,model_hinselmann,model_hpv,model_schiller]
    for i in range(7):
        prediction = test_list[i].predict(data_unseen_scaled[i])[0]
        if prediction == 0:
            test_result[i] ="You are safe for now :)"
        else:
            test_result[i] = "You might have high risk of having cervical cancer"
        con_level[i]= max(max((test_list[i].predict_proba(data_unseen_scaled[i])))) * 100
    #fig = graph.figure()
    #ax = fig.add_axes([0, 0, 1, 1])
    #test_name = ['dx: Cancer', 'dx: CIN', 'dx: HPV', 'Citology', 'Hinselmann', 'Schiller', 'Biopsy', 'Hinselmann']
    #ax.bar(test_name, test_result)
    #graph.show()
    return render_template('index.html', prediction_text="""
    Accorrding to dx:Cancer test {}. Confidence level:{}%
    Accorrding to Biopsy test {}. Confidence level: {}% 
    Accorrding to dx:CIN test {}. Confidence level: {}% 
    Accorrding to Citology test {}. Confidence level: {}% 
    Accorrding to Hinselmann test {}. Confidence level: {}%  
    Accorrding to dx:HPV test {}. Confidence level: {}% 
    Accorrding to Schiller test {}. Confidence level: {}% 
                                                        
                                                        """.format(
        test_result[0], con_level[0],
        test_result[1], con_level[1],
        test_result[2], con_level[2],
        test_result[3], con_level[3],
        test_result[4], con_level[4],
        test_result[5], con_level[5],
        test_result[6], con_level[6]))

if __name__ == "__main__":
    app.run(debug=True)