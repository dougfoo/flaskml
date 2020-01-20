from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)
models = {}
# models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')

print('loaded models', models)


@app.route('/', methods=['GET'])
def base():
    return '<div>Welcome to the Flask ML Runner -- paths available:  /models/<modelName> where modelName is one of the registered models:<P/><P/><PRE> ' + str(models)+'</PRE></div>'

# NLP sentiment analysis section


analyser = SentimentIntensityAnalyzer()

# NLP sentiment + evaluators
@app.route('/nlp/sa/<model>', methods=['GET'])
def sa_predict(model):
    sentence = request.args.get('data')
    print(sentence)

    if (model == 'all'):
        data = {}
        data['input'] = sentence
        data['vader'] = vader(sentence)
        data['textblob'] = textblob(sentence)
        data['azure'] = azure_sentiment(sentence)
        data['google'] = gcp_sentiment(sentence)

        return json.dumps(data)
    elif (model == 'azure'):
        return azure_sentiment(sentence)
    elif (model == 'vader'):
        return vader(sentence)
    elif (model == 'textblob'):
        return textblob(sentence)
    elif (model == 'google'):
        return gcp_sentiment(sentence)
    else:
        return 'No Model exists for '+model


def textblob(sentence):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(sentence)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive ' + str(analysis.sentiment.polarity)
    elif analysis.sentiment.polarity == 0:
        return 'neutral 0'
    else:
        return 'negative ' + str(analysis.sentiment.polarity)


def vader(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))
    return str(score)


# azure and google copies from:  https://www.pingshiuanchua.com/blog/post/simple-sentiment-analysis-python?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com

# google cloud
def gcp_sentiment(text):
    import requests

    gcp_url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyBN-SLv7YPAMARDo2eQl7Y_yyy84xpWcHU"

    document = {'document': {'type': 'PLAIN_TEXT', 'content': text}, 'encodingType':'UTF8'}
    response = requests.post(gcp_url, json=document)
    sentiments = response.json()
    return sentiments

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
    import requests
    documents = {'documents': [
        {'id': '1', 'text': text}
    ]}

    azure_key = 'd6c00eb74e58455187125aa6a97fd976'  # Update here
    # Update here  https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment
    azure_endpoint = 'https://textsentimentanalyzer.cognitiveservices.azure.com/text/analytics/v2.1/'
#    azure_endpoint = 'https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/' # Update here  https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment

    assert azure_key
    sentiment_azure = azure_endpoint + '/sentiment'

    headers = {"Ocp-Apim-Subscription-Key": azure_key}
    response = requests.post(sentiment_azure, headers=headers, json=documents)
    sentiments = response.json()
    return sentiments

# azure_results = [azure_sentiment(text) for text in dataset]
# azure_score = [row['documents'][0]['score'] for row in azure_results] # Extract score from the dict
# azure = list(zip(dataset, azure_score))
# columns = ['text', 'score']
# azure_df = pd.DataFrame(azure, columns = columns)


if __name__ == '__main__':
    app.run(debug=True)
