import sys

from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np

from Model import lr, model_columns

app = Flask(__name__)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(lr.predict(query))

            return jsonify({'prediction': str(prediction)})

        except:
            # return jsonify({'trace': traceback.format_exc()})
            return "no call"
    else:
        print('Train the model first')
        return 'No model here to use'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 5000  # If you don't provide any port the port will be set to 12345

    lr = joblib.load("model.pkl")  # Load "model.pkl"
    print('Model loaded')
    model_columns = joblib.load("model_columns.pkl")  # Load "model_columns.pkl"
    print('Model columns loaded')

    app.run(port=port, debug=True)
