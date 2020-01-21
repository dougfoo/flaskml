from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
from sklearn.externals import joblib
from flask_cors import CORS
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from flask import Flask, request, redirect, url_for, flash, jsonify, render_template
import numpy as np
import requests
#mport azureml.train.automl

#
# XGB2, ISO, LR3, RF are all from sklearn and have common input formats (18 features onehot)
# LBGM has 4 features not onehot, [carat, color, cut, clarity]
#

app = Flask(__name__, static_url_path='/web')
CORS(app)

models = {}
models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')
models['ISO'] = joblib.load('models/sklearn_diamond_iso_model.pkl')
models['LR3'] = joblib.load('models/sklearn_diamond_regr_model.pkl')
models['RF'] = joblib.load('models/sklearn_diamond_rforest_model.pkl')
#models['LBGM'] = joblib.load('models/az_automodel2.pkl')

print('loaded models', models)

@app.route('/', methods=['GET'])
def base():
	return '<div>Welcome to the Flask ML Runner -- paths available:  /models/<modelName> where modelName is one of the registered models:<P/><P/><PRE> ' +str(models)+'</PRE></div>'

@app.route("/web")
def index():
   return render_template("sa_gui/web/index.html")

# ML diamond predict models
@app.route('/models/<model>', methods=['POST'])
def predict(model):
	if (models.get(model) is None):
		print('model not found: ',model)
		return jsonify("[-1]")

	j_data = np.array(request.get_json()['data'])
	y_hat = np.array2string(models[model].predict(j_data))
	print('input: ',j_data, ', results:', y_hat)
	return y_hat

# sentiment analysis module /nlp/sa/

# NLP sentiment analysis section
# merge to common format:
#  {
#    "input": "I love the world so much",
#    "results": [
#       {
#        "model": "AzureML",
#        "nScore": 0.8,  # -1.0 to +1.0 w/ 1.0 being positive, -1.0 negative, 0.0 neutral
#        "rScore": .5,  # raw results in case it is -0.5 to 0.5 or -1 to +1
#        "extra": "na optional text only"#
#       },
#       ...
#     ]
#  }
print('loading nlp_mod - sentiment analysis modules /nlp/sa/all?data=query')

@app.route('/nlp/sa/<model>', methods=['GET'])
def sa_predict(model):
	sentence = request.args.get('data')
	print(sentence)

	resp = {}
	resp['input'] = sentence
	resp['results'] = []

	if (model == 'all'):
		resp['results'].append(vader(sentence))
		resp['results'].append(textblob(sentence))
		resp['results'].append(azure_sentiment(sentence))
		resp['results'].append(gcp_sentiment(sentence))
	elif (model == 'azure'):
		resp['results'] = azure_sentiment(sentence)
	elif (model == 'vader'):
		resp['results'] = vader(sentence)
	elif (model == 'textblob'):
		resp['results'] = textblob(sentence)
	elif (model == 'google'):
		resp['results'] = gcp_sentiment(sentence)
	else:
		# flag error 
		return 'No Model exists for '+model
	return json.dumps(resp)

def textblob(sentence):
	resp = {}
	resp['model'] = 'TextBlob'
	resp['extra'] = 'https://textblob.readthedocs.io/en/dev/ - models returns -1 to +1'
	# create TextBlob object of passed tweet text
	analysis = TextBlob(sentence)
	resp['rScore'] = analysis.sentiment.polarity
	resp['nScore'] = analysis.sentiment.polarity
	# set sentiment
	return resp

def vader(sentence):
	resp = {}
	resp['model'] = 'Vader'
	resp['extra'] = 'https://pypi.org/project/vaderSentiment/ - model returns -1 to +1'
	analyser = SentimentIntensityAnalyzer()
	score = analyser.polarity_scores(sentence)['compound'] 
	resp['rScore'] = score
	resp['nScore'] = score
	return resp


# azure and google inspired from:  https://www.pingshiuanchua.com/blog/post/simple-sentiment-analysis-python?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com

# google cloud
##
def gcp_sentiment(text):
	resp = {}
	resp['model'] = 'Google NLP'
	resp['extra'] = 'https://cloud.google.com/natural-language/ - model returns -1 to +1'

	gcp_url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyBN-SLv7YPAMARDo2eQl7Y_yyy84xpWcHU"

	document = {'document': {'type': 'PLAIN_TEXT', 'content': text}, 'encodingType':'UTF8'}
	response = requests.post(gcp_url, json=document)
	sentiments = response.json()
	score = sentiments['documentSentiment']['score']

	resp['rScore'] = score
	resp['nScore'] = score 
	return resp

# azure service calls
##
def azure_sentiment(text):
	resp = {}
	resp['model'] = 'Azure NLP'
	resp['extra'] = 'https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/ - model returns 0 to 1'

	documents = {'documents': [
		{'id': '1', 'text': text}
	]}

	azure_key = 'd6c00eb74e58455187125aa6a97fd976'  # Update here
	azure_endpoint = 'https://textsentimentanalyzer.cognitiveservices.azure.com/text/analytics/v2.1/'
	sentiment_azure = azure_endpoint + '/sentiment'

	headers = {"Ocp-Apim-Subscription-Key": azure_key}
	response = requests.post(sentiment_azure, headers=headers, json=documents)
	score = response.json()['documents'][0]['score']

	resp['rScore'] = score
	resp['nScore'] = 2 * (score - 0.5) 

	return resp


if __name__ == '__main__':
    app.run(debug=True)
