import joblib
import numpy as np

def cust_input(dict_input):
    data = []
    for _, value in dict_input.items():
        data.append(float(value))
    return np.array(data).reshape(1,-1)

def rf_predict(input_data):
    with open('random_forest.joblib', 'rb') as f:
        model = joblib.load(f)
    return np.round(model.predict_proba(input_data)[0]*100,3)

