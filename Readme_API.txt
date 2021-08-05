SOME SUGGESTIONS FOR THE DEChallengeModel.ipynb

The file DEChallengeModel.ipynb is a jupiter notbook where the model was developed. I suggest:

I:    Add the version of python and all import libraries.
II:   Add some comments in this file may facilitate the reading and understanding for everyone. For example 
      the general idea of the model or of the blocks.
III:  Add  a .txt file with the characteristics and the content for the variables of the database. 




API 
My api runs on port 4000  from host 0.0.0.0 and it has three main routes:
1. http://localhost:4000/
   This is the front page that welcomes the users. Also, help me to know that the server was created

2. http:/localhost:4000/EmployeeNumber
   This route  uses the EmployeeNumber to load its turnover probability stored in  data_set

3. http:/localhost:4000/evaluate
   This route works with  http-POST request where the  sent data  is a json file, such as:
   [
    {"Age":37, "BusinessTravel":"Travel_Frequently", "DailyRate":29, 
    "Department":"Research & Development", "DistanceFromHome":12, "Education":3, 
    "EducationField":"Life Sciences", "EmployeeNumber":23333999, "EnvironmentSatisfaction":13, 
    "Gender":"Male", "HourlyRate":61, "JobInvolvement":2, "JobRole":"Research Scientist", 
    "JobSatisfaction":2, "MaritalStatus":"Married", "MonthlyIncome":5130, 
     "MonthlyRate":24907, "NumCompaniesWorked":1, "OverTime":"No", "PercentSalaryHike":23, 
     "PerformanceRating":4, "RelationshipSatisfaction":4, "StockOptionLevel":1, 
     "TrainingTimesLastYear":3,  "WorkLifeBalance":3, "YearsAtCompany":10, 
     "YearsInCurrentRole":1, "YearsSinceLastPromotion":1, "YearsWithCurrManager":1}
   ]
   This information is sent to the random forest classification model to predict the turnover probability
   for a new employee.
    




API TEST

I used insmonia to test my api and it works well!
I played with the model and noticed that in the third case (POST)
    -  The entry order is important because if you switch two or more entries the code sent an error
    -  The entry types are important. I mean, if you sent a string in-place of an expected int the code 
       sent a error.
    -  The number of entries must to correspond to the expected by the model. For example if
       you erase "Age":37 in the  setn data, the code display an error.
