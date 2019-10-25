from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)
models = {}
    
@app.route('/models/<model>', methods=['POST'])
def predict(model):
	if (models.get(model) is None):
		print('model not found: ',model)
		return jsonify("[-1]")

	j_data = np.array(request.get_json()['data'])
	y_hat = np.array2string(models[model].predict(j_data))
	print('input: ',j_data, ', results:', y_hat)
	return y_hat

if __name__ == '__main__':
    models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')
    models['ISO'] = joblib.load('models/sklearn_diamond_iso_model.pkl')
    models['LR3'] = joblib.load('models/sklearn_diamond_regr_model.pkl')
    models['RF'] = joblib.load('models/sklearn_diamond_rforest_model.pkl')
    print('loaded models', models)
    app.run(debug=True,host='0.0.0.0')