import pickle
from flask import Flask, request, jsonify, render_template
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Create app
app = Flask(__name__)

# Load model and scaler
regmodel = pickle.load(open('mlr.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))
    output = regmodel.predict(final_input)[0]
    return render_template("home.html", prediction_text=f"The house price is {output:.2f}")

@app.route('/eda')
def eda():
    # Generate EDA plots
    df = pd.read_csv('boston_data.csv')  # Assume you saved the dataset as CSV
    img = BytesIO()
    sns.pairplot(df)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('eda.html', plot_url=plot_url, summary=df.describe().T.to_html())

if __name__ == "__main__":
    app.run(debug=True)
