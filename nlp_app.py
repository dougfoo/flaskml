from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import requests
from flask_cors import CORS
from sklearn.externals import joblib

app = Flask(__name__)
CORS(app)

models = {}
# models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')

print('loaded models', models)


@app.route('/', methods=['GET'])
def base():
    return '<div>Welcome to the Flask ML Runner -- paths available:  /models/<modelName> where modelName is one of the registered models:<P/><P/><PRE> ' + str(models)+'</PRE></div>'

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


# azure and google copies from:  https://www.pingshiuanchua.com/blog/post/simple-sentiment-analysis-python?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com

# google cloud
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

# from tqdm import tqdm # This is an awesome package for tracking for loops
# import pandas as pd
# gc_results = [gc_sentiment(row) for row in tqdm(dataset, ncols = 100)]
# gc_score, gc_magnitude = zip(*gc_results) # Unpacking the result into 2 lists
# gc = list(zip(dataset, gc_score, gc_magnitude))
# columns = ['text', 'score', 'magnitude']
# gc_df = pd.DataFrame(gc, columns = columns)


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

# azure_results = [azure_sentiment(text) for text in dataset]
# azure_score = [row['documents'][0]['score'] for row in azure_results] # Extract score from the dict
# azure = list(zip(dataset, azure_score))
# columns = ['text', 'score']
# azure_df = pd.DataFrame(azure, columns = columns)


if __name__ == '__main__':
    app.run(debug=True)
