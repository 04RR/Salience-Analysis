import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"sentiment-analysis-284609-a234a6af795c.json.json"


def language_analysis(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    ent_analysis = client.analyze_entities(
        document=document, encoding_type='UTF32')
    dir(ent_analysis)
    entities = ent_analysis.entities
    return sentiment, entities


text = sys.argv[1]
# text = 'Artificial neural networks, usually simply called neural networks, or connectionist systems are computing systems vaguely inspired by the biological neural networks that constitute animal brains. The data structures and functionality of neural nets are designed to simulate associative memory.'
items = []
sentiment, entities = language_analysis(text)

dicti = {}
for e in entities:
    print(f'Word: {e.name}\nType: {e.type}\nSalience: {round(e.salience,2)}\n')

print(f'Sentiment\n{sentiment}')
