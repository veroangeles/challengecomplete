#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Created on Tue Aug  3 13:30:41 2021
#@author: veronicaangeles <huraenet@gmail.com>
'''
library versions
Flask==2.0.1
joblib==1.0.1
pandas==1.3.1
numpy==1.21.1
json5==0.9.6

'''

"""
This code is for an API to return the probability of turnover given a set a characteristics like age, etc.
The API has three routes:
/ :                     welcome message
/<string:worker_ID> :   consult the turnover probability for an existing worker ID in the data-base
/evaluate:              consult the turnover probability for an new worker according with the model.
"""




from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import json
import math





app = Flask(__name__)
'''server aplication that asign to app object '''
@app.route('/')
def welcome():
    return "<h1 style='color:blue;'> Welcome to HR turnover score API</h1> <p>This API calculates the turnover probability for (a) an existing employee. Also, (b) it suggests if the worker will probably turnover. Finally, with the aid of an API client, (c) we can get the turnover propability for a new employee. </p> <p>SYNTAX:</p>  <p>(a) type http://localhost:4000/ID where ID stands for the employee number of an employee.</p> <p>(c) type http://localhost:4000/sug/ID where ID stands for the employee number of an employee.</p> <p>(c) In the API client, we request http://localhost:4000/evaluate with the POST method. Posted data must have an especial structure, see Readme_API.txt file for more info."



@app.route('/<string:worker_ID>')
def get_ID(worker_ID):
    try: 
        '''To say server get the 'worker_ID' and search the score for it
        '''
        result = data_set.loc[int(worker_ID)].turnover_score
        result = round(result,2)
        output = {'worker_ID': worker_ID, 'score': str(result)}
        return jsonify(output)
    except:
        '''Sent a message if the worker_ID does not exist
        '''
        return '<h2 style= "color:red">This  Employee Number was not find, try with another.</h2>'


@app.route('/sug/<string:worker_ID>')
def sug_ID(worker_ID):
    try: 
        '''To say server get the 'worker_ID' and search the score for it
        '''
        result = data_set.loc[int(worker_ID)].turnover_score
        result = round(result,2)
        suggestion= 'yes' if result>0.5 else 'no'
        output = {'worker_ID': worker_ID, 'turnover': suggestion}
        #return json.dumps(output)
        return jsonify(output)
    except:
        '''Sent a message if the worker_ID does not exist
        '''
        return '<h2 style= "color:red">This  Employee Number was not find, try with another.</h2>'


@app.route('/evaluate',methods=['POST'])
def predict():
    '''to say server read  the data  and use the model to predict the turnover-score for a new worker '''
    json_= request.get_json()
    data_frame = pd.DataFrame(json_)
    # transfor to numpy.int64 to integer
    ID = int(data_frame['EmployeeNumber'][0])
    data_frame.drop(columns = ['EmployeeNumber'], inplace=True)
    #use the model to predict the probability for new worker
    prediction = model.predict_proba(data_frame)
    turn_over_prob=round(list(prediction[:,1])[0],2)
    suggestion= 'yes' if turn_over_prob>0.5 else 'no'
    output ={'worker_ID': ID, 'score':turn_over_prob,'turnover':suggestion}
    return jsonify(output)
    # I suggest to display a color bar, where map the probability from 0 to 100%



if __name__=='__main__':
    

    modelfile = 'clf.model'
    #load the model of the forest tree
    model = joblib.load(modelfile)
    
    data = 'data_set.pkl'
    data_set=joblib.load(data)
    # set  EmployeeNumber as index
    data_set.set_index('EmployeeNumber',inplace= True)
    
    
    #staritng to run the app in port 4000
    app.run(host='0.0.0.0', port=4000, debug=True)

    