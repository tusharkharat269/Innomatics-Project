from flask import Flask, render_template, request
import joblib
import pandas as pd
import io

app = Flask(__name__)

# Load pre-trained machine learning model
# model = joblib.load('model/logistic_regression.pkl')
model = joblib.load('model/naive_bayes.pkl')

# Define function to process user input and make predictions
def predict_sentiment(input_data):
    if input_data.endswith('.csv'):
        df = pd.read_csv(io.StringIO(input_data))
        X = df['review_text']
        predictions = model.predict(X)
        return zip(df['review_text'], predictions)
    else:
        prediction = model.predict([input_data])[0]
        # print(prediction)

        if  prediction == 'Positive':
            return [(input_data, 1)]
        else:
            return [(input_data, 0)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = request.form['input_data']
        predictions = predict_sentiment(input_data)
        # print(predictions)
        return render_template('result.html', predictions=predictions)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
