#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 22:41:01 2021 
library versions
Flask==2.0.1
joblib==1.0.1
pandas==1.3.1
numpy==1.21.1
json5==0.9.6
scikit-learn==0.24.2

@author: veronicaangeles <huraenet@gmail.com>
This file is only for the MODEL, it allow us to know the probabilit of a employee turnover
"""



'''
IMPORT LIBRARIES
'''


#Processing data
#import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split #for split the data for random forest
from sklearn.preprocessing import OrdinalEncoder

#the method of algorithm to entrain 
from sklearn.ensemble import RandomForestClassifier # random forest clearly

#create a pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

#To measure the entrained results
from sklearn import metrics

#Save the model
import joblib


'''
SPLIT DATA FOR TESTING AND TRAINING
'''

#reading the csv file with de data.
hrdata = pd.read_csv('HR_Employee_Attrition.csv')

#only to know how many na in each column are
#print(hrdata.isna().sum())
#there are not na

#types of columns
#print(hrdata.dtypes)

#some  statistical data
#print(hrdata.describe)



#Build a train data from the original data
train_hrdata = hrdata.drop(columns=['EmployeeCount','EmployeeNumber','JobLevel', 
                                    'Over18', 'StandardHours', 'TotalWorkingYears'])

#transform the column called  "Attrition" from to categorical to binary(numeric)
#because RF classifier needs numercial varibles to input 
train_hrdata['Attrition'] = train_hrdata.Attrition.map({'Yes':1,
                                              'No':0})


#list of categorical attributes
categorical_attributes = ['BusinessTravel', 'OverTime',
                          'Department', 'EducationField', 
                          'Gender','JobRole','MaritalStatus']


#########Using the random forest method for clasification ##############

#create the trees 
rf = RandomForestClassifier(max_depth=12,      #max depth in the tree
                            max_features=11,   #number of predictors in each step
                            n_estimators=180,  #numbers of trees
                            random_state=2021, #seed for generate random 
                            n_jobs=-1)         #utilize all the cores 


cat_pipe = ColumnTransformer([('ordinal_encoder', OrdinalEncoder(), categorical_attributes)],
                             remainder='passthrough')

pipe_model = Pipeline([
      ('encoder', cat_pipe),
      ('classification', rf )
    ])

df1=  train_hrdata[train_hrdata.Attrition==0].sample(600).reset_index(drop=True)
df2=  train_hrdata[train_hrdata.Attrition == 1]
train_set = pd.concat([df1 , df2 , df2] , axis=0).reset_index(drop=True)

#split the data into independent "x" an dependent "y" variables
x = train_set.drop('Attrition',1) ### Drop before having the target variable
y = train_set['Attrition']


#print(x.shape)
#print(y.shape)

#split the data set into 80% training set and 20% testing set
x_train, x_test, y_train, y_test = train_test_split(x,y, 
                                                    random_state=2021, 
                                                    test_size=0.2,
                                                    stratify =y)
'''USING THE RANDOM FOREST METHOD FOR CLASIFICATION'''
pipe_model.fit(x_train, y_train) #training
y_pred = pipe_model.predict(x_test) #apply predict method to test with testing data

#get the accuracy on the testing data
print('Accuracy Score of Random Forest Classifier is: ', metrics.accuracy_score(y_test, y_pred))
print('Recall Score of Random Forest Classifier Model is: ', metrics.recall_score(y_test, y_pred))

print(metrics.classification_report(y_test, y_pred))
val_cols = list(train_set.columns)
val_cols.remove('Attrition')

#add column with the probability if employee turnover==1
hrdata["turnover_score"] = pipe_model.predict_proba(hrdata[val_cols])[:,1]


#hrdata[['EmployeeNumber','turnover_score']].head(2)


'''
SAVE MODEL
'''

joblib.dump(pipe_model, 'clf.model')


'''
SAVE PARTIAL DATA SET
'''

joblib.dump(hrdata,'data_set.pkl')


'''
SAVE COLABORATORS ID
'''
ID_LIST=list(hrdata['EmployeeNumber'])
joblib.dump(ID_LIST,'id_list.pkl')
#clf = joblib.load('clf.model')