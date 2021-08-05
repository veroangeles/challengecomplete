
try:
    from app import app
    import unittest
    import json
    import requests
    import joblib
    from numpy.random import choice
   
except Exception as e:
    print("somemodules are missing{}".format(e))


class FlaskTest(unittest.TestCase):
    
    #Check if response is 200
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('http://localhost:4000/')
        statuscode=response.status_code
        self.assertEqual(statuscode,200)
     
    def test_index_ID(self):
        tester=app.test_client(self)
        response=tester.get('http://localhost:4000/5')
        statuscode=response.status_code
        self.assertEqual(statuscode,200)
     
    def test_index_sug(self):
        tester=app.test_client(self)
        response=tester.get('http://localhost:4000/sug/5')
        statuscode=response.status_code
        self.assertEqual(statuscode,200)
     
    def test_index_mm(self):
        payload = [{"Age":37, "BusinessTravel":"Travel_Frequently", "DailyRate":29, "Department":"Research & Development", "DistanceFromHome":12, "Education":3, "EducationField":"Life Sciences", "EmployeeNumber":23333999, "EnvironmentSatisfaction":13, "Gender":"Male", "HourlyRate":61, "JobInvolvement":2, "JobRole":"Research Scientist", "JobSatisfaction":2, "MaritalStatus":"Married", "MonthlyIncome":5130,  "MonthlyRate":24907, "NumCompaniesWorked":1, "OverTime":"No", "PercentSalaryHike":23, "PerformanceRating":4, "RelationshipSatisfaction":4, "StockOptionLevel":1, "TrainingTimesLastYear":3,  "WorkLifeBalance":3, "YearsAtCompany":10, "YearsInCurrentRole":1, "YearsSinceLastPromotion":1, "YearsWithCurrManager":1}]
        headers = {'content-type': 'application/json'}
        response=requests.post('http://localhost:4000/evaluate',data=json.dumps(payload),headers=headers)
        statuscode=response.status_code
        self.assertEqual(statuscode,200)            

    #Check for data return

    def test_content_ID(self):
        tester=app.test_client(self)
        response=requests.get('http://localhost:4000/5')
        self.assertTrue('score' in response.text)
     
    def test_content_sug(self):
        response=requests.get('http://localhost:4000/sug/5')
        self.assertTrue('turnover' in response.text)
     
    def test_content_mm(self):
        payload = [{"Age":37, "BusinessTravel":"Travel_Frequently", "DailyRate":29, "Department":"Research & Development", "DistanceFromHome":12, "Education":3, "EducationField":"Life Sciences", "EmployeeNumber":23333999, "EnvironmentSatisfaction":13, "Gender":"Male", "HourlyRate":61, "JobInvolvement":2, "JobRole":"Research Scientist", "JobSatisfaction":2, "MaritalStatus":"Married", "MonthlyIncome":5130,  "MonthlyRate":24907, "NumCompaniesWorked":1, "OverTime":"No", "PercentSalaryHike":23, "PerformanceRating":4, "RelationshipSatisfaction":4, "StockOptionLevel":1, "TrainingTimesLastYear":3,  "WorkLifeBalance":3, "YearsAtCompany":10, "YearsInCurrentRole":1, "YearsSinceLastPromotion":1, "YearsWithCurrManager":1}]
        headers = {'content-type': 'application/json'}
        response=requests.post('http://localhost:4000/evaluate',data=json.dumps(payload),headers=headers)
        self.assertTrue('score' in response.text)   
    #test for non existing colaborator
    def test_non_sug(self):
        response=requests.get('http://localhost:4000/sug/3')
        self.assertFalse('turnover' in response.text)
    def test_non(self):
        response=requests.get('http://localhost:4000/3')
        self.assertFalse('score' in response.text)

# Two iterative test for testing http://localhost:4000/ and http://localhost:4000/sug
# at three randomly selected colaborators
def test_generator(a):
    def test(self):
        tester=app.test_client(self)
        response=tester.get('http://localhost:4000/'+str(a))
        statuscode=response.status_code
        self.assertEqual(statuscode,200)      
    return test  
def test_generator2(a):
    def test(self):
        tester=app.test_client(self)
        response=tester.get('http://localhost:4000/sug/'+str(a))
        statuscode=response.status_code
        self.assertEqual(statuscode,200)      
    return test  


if __name__=="__main__":
    #I import the list of the colaborator ids
    data = 'id_list.pkl'
    lista=joblib.load(data)
    #Randomly selecting three colaborator ids for testing
    test_list=choice(lista,3)
    #run the test
    for t in test_list:
        test_name = 'test_%s' % t
        test_name2 = 'test_sug%s' % t
        test = test_generator(t)
        test2 = test_generator2(t)
        setattr(FlaskTest, test_name, test)
        setattr(FlaskTest, test_name2, test2)
    unittest.main()