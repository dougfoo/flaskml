from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)
models = {}
# models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')

print('loaded models', models)

@app.route('/', methods=['GET'])
def base():
	return '<div>Welcome to the Flask ML Runner -- paths available:  /models/<modelName> where modelName is one of the registered models:<P/><P/><PRE> ' +str(models)+'</PRE></div>'

# NLP sentiment analysis section

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
from textblob import TextBlob 

# NLP sentiment + evaluators
@app.route('/nlp/sa/<model>', methods=['GET'])
def sa_predict(model):
	sentence = request.args.get('data')

	if (model == 'vader'):
		score = analyser.polarity_scores(sentence)
		print("{:-<40} {}".format(sentence, str(score)))
		return str(score)
	elif (model == 'textblob'):
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(sentence) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive ' + str(analysis.sentiment.polarity)
		elif analysis.sentiment.polarity == 0: 
			return 'neutral 0'
		else: 
			return 'negative '+ str(analysis.sentiment.polarity)
	else:
		return 'No Model exists for '+model



## azure and google copies from:  https://www.pingshiuanchua.com/blog/post/simple-sentiment-analysis-python?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com

## google cloud
def gc_sentiment(text):  
    from google.cloud import language
    
    path = '/Users/Yourname/YourProjectName-123456.json' #FULL path to your service account key
    client = language.LanguageServiceClient.from_service_account_json(path)
    document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    return score, magnitude

# from tqdm import tqdm # This is an awesome package for tracking for loops
# import pandas as pd
# gc_results = [gc_sentiment(row) for row in tqdm(dataset, ncols = 100)]
# gc_score, gc_magnitude = zip(*gc_results) # Unpacking the result into 2 lists
# gc = list(zip(dataset, gc_score, gc_magnitude))
# columns = ['text', 'score', 'magnitude']
# gc_df = pd.DataFrame(gc, columns = columns)


## azure service calls
##
def azure_sentiment(text):
    import requests
    documents = { 'documents': [
            { 'id': '1', 'text': text }
            ]}
    
    azure_key = '[your key]' # Update here
    azure_endpoint = '[your endpoint]' # Update here
    assert azure_key
    sentiment_azure = azure_endpoint + '/sentiment'
    
    headers   = {"Ocp-Apim-Subscription-Key": azure_key}
    response  = requests.post(sentiment_azure, headers=headers, json=documents)
    sentiments = response.json()
    return sentiments

# azure_results = [azure_sentiment(text) for text in dataset]
# azure_score = [row['documents'][0]['score'] for row in azure_results] # Extract score from the dict
# azure = list(zip(dataset, azure_score))
# columns = ['text', 'score']
# azure_df = pd.DataFrame(azure, columns = columns)



if __name__ == '__main__':
    app.run(debug=True)