import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"sentiment-analysis-284609-a234a6af795c.json"

def language_analysis(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    ent_analysis = client.analyze_entities(
        document=document, encoding_type='UTF32'
    )
    response = client.classify_text(document)
    dir(ent_analysis)
    entities = ent_analysis.entities
    
    type_ = enums.Document.Type.PLAIN_TEXT
    lan = "en"
    document = {"content": text, "type": type_, "language": lan}

    response = client.classify_text(document)
    #categories = ent_analysis.categories
    return sentiment, entities, response.categories

text = sys.argv[1]

sentiment, entities, categories = language_analysis(text)
typess = {1:'Person', 2:'Location', 3:'Organisation', 4:'Event', 5:'Work of Art', 6:'CONSUMER GOOD', 7:'Other', 8:'Other', 9:'Other', 10:'Other', 11:'Date', 12:'Number', 13:'Price'}

for e in entities:
    print(f'Word: {e.name}\nType: {typess[e.type]}\nSalience: {round(e.salience,2)}\n')

print(f'Sentiment\n{sentiment}')
print('Categories')
for cat in categories:
    print(f'{cat.name} with {round(cat.confidence, 2)*100}% confidence')

