import json
import os
import pickle
import numpy as np
from sklearn.externals import joblib
from azureml.core.model import Model

def init():
    global model
    # retrieve the path to the model file using the model name
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'sklearn_diamond_iso_model.pkl')
#    model_path = Model.get_model_path('sklearn_diamond_simple_model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    # make prediction
    y_hat = model.predict(data)
    # you can return any data type as long as it is JSON-serializable
    return y_hat.tolist()


# input_sample = np.array([[4, 3, 2, 1]])
# output_sample = np.array([3726.995])

# note you can pass in multiple rows for scoring
# @input_schema('data', NumpyParameterType(input_sample))
# @output_schema(NumpyParameterType(output_sample))


