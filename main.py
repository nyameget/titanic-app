from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

model = pickle.load(open('rnd_model.pkl', 'rb'))

# These are url endpoints
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        pclass = int(request.form['pclass'])
        age = int(request.form['age'])
        fare = float(request.form['fare'])
        sex = int(request.form['sex'])
        dic = {
            'Pclass': pclass,
            'Sex': sex,
            'Age': age,
            'Fare': fare
        }
        df = pd.DataFrame(dic, index=[0])
        prediction = model.predict(df)
        survive = ''
        gender = ''
        if sex == 0:
            gender = 'Male'
        else:
            gender = 'Female'

        if prediction[0] == 1:
            survive = 'Yes'
        else: 
            survive = 'No'

        info = {
            'Pclass': pclass,
            'Sex': gender,
            'Age': age,
            'Fare': fare,
            'Survived': survive
        }
        page = 'prediction.html'
    except:
        #info = {
        #    'Title': 'Invalid Inputs Try again',
        #    'data': {
        #        'Pclass': 'Must be an integer',
        #        'Age': 'Must be an integer',
        #       'Fare': 'Must be a float'
        #   }
        #}
        info = 'Fail'
        page = 'index.html'
    return render_template(page, data=info)


if __name__ == '__main__':
    app.run(debug=True)
