"""

------------------SENTIMENT ANALYSIS---------------------


"""

key = "c268c7f360854a62ae033b75205b916c"
endpoint = "https://openbooknlp.cognitiveservices.azure.com/"

# from azure.ai.textanalytics import single_analyze_sentiment
# from azure.ai.textanalytics import single_detect_language
# from azure.ai.textanalytics import single_recognize_entities

from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

documents = [
    "I did not like the restaurant. The food was too spicy. I had such a horrible time there I feel depressed as I was lonely.",
    "I feel amazeballs today. Such a wonderful time at these hackathons! Happiest day of my life!",
    "Mala kahich mahit nahi kay challay ithe?"
]
def detect_language(documents):
        # [START batch_detect_language]
        result = text_analytics_client.detect_language(documents)
        text = []
        for idx, doc in enumerate(result):
            if not doc.is_error:
                text.append("Document text: {}".format(documents[idx]))
                
                text.append("Language detected: {}".format(doc.primary_language.name))
                text.append("ISO6391 name: {}".format(doc.primary_language.iso6391_name))
                text.append("Confidence score: {}\n".format(doc.primary_language.score))
            if doc.is_error:
                text.append(doc.id)
                text.append(doc.error)
        return "<br>".join(text)
        # [END batch_detect_language]

def extract_key_phrases(documents):
        # [START batch_extract_key_phrases]
        
        text = []
        result = text_analytics_client.extract_key_phrases(documents)
        for doc in result:
            if not doc.is_error:
                text.append("<br>".join(doc.key_phrases))
            elif doc.is_error:
                text.append(doc.id)
                # text.append(doc.error) 

        return "<br>".join(text)
        # [END batch_extract_key_phrases]

def analyze_sentiment(documents):
        # [START batch_analyze_sentiment]
        result = text_analytics_client.analyze_sentiment(documents)
        # print(result)
        docs = [doc for doc in result if not doc.is_error]

        text = []

        for idx, doc in enumerate(docs):
            text.append("Entry: {}".format(documents[idx]))
            text.append("Sentiment: {}".format(doc.sentiment))
        # [END batch_analyze_sentiment]
            text.append("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
                doc.sentiment_scores.positive,
                doc.sentiment_scores.neutral,
                doc.sentiment_scores.negative,
            ))
            for idx, sentence in enumerate(doc.sentences):
                text.append("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
                text.append("Sentence score: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f}".format(
                    sentence.sentiment_scores.positive,
                    sentence.sentiment_scores.neutral,
                    sentence.sentiment_scores.negative,
                ))
                text.append("Offset: {}".format(sentence.offset))
                text.append("Length: {}\n".format(sentence.length))
            text.append("------------------------------------------------------")

        return ''.join(text)

"""

----------FLASK APP FROM HERE---------------------


"""
from flask import Flask
from datetime import datetime
from flask import render_template, request
import re
import os
from ocr import return_ocr

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html",result_string='',date=datetime.now(),txt_entry='')


@app.route('/result',methods = ['POST'])
def result():
   if request.method == 'POST':
      result = request.form.get('paragraph_text')
      documents = result.split('.')
      print(documents)
      result_string = analyze_sentiment(documents) + extract_key_phrases(documents)
      return render_template("home.html",result_string=result_string,date=datetime.now(),txt_entry='')

@app.route('/ocr',methods = ['POST','GET'])
def ocr():
    if request.method == 'POST':
        APP_ROOT = os.getcwd()
        target = os.path.join(APP_ROOT, 'static\image')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            filename = file.filename
            destination = "\\".join([target, filename])
            file.save(destination)
            print('destination is \n\n\n\n\n\n\n',destination)
            text, lines = return_ocr(destination)
            print('\n\n\n\n\n\n\n\n\n',lines)
            print('\n\n\n\n\n\n\n\n\n',text)

    return render_template("home.html",txt_entry=text,date=datetime.now())

@app.route("/test")

def test():
    sen = request.args.get('sen')
    confidence = request.args.get('confidence')

    return "your sentiment is {} with confidence score {}".format(sen,confidence)


# @app.route("/new")
# def new():
#     journal = request.args.get('Param')
#     documents=[journal]
#     print (documents)
#     return   analyze_sentiment(documents) + extract_key_phrases(documents) #+ detect_language(documents)

    # extract_key_phrases(documents)
    # analyze_sentiment(documents)
    # detect_language(documents)
    # print (journal)
    

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
# '127.0.0.1', port=8080,

# @app.route("/api/data")
# def get_data():
#     return app.send_static_file("data.json")