from flask import Flask
import requests
from flask import Response
import json


from ocp import *
app = Flask(__name__)

@app.route('/')
def index():
    ocr_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr'
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"
    subscription_key = '674c2a16cc18418fb514d1df71071490'
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
    params   = {'language': 'unk', 'detectOrientation ': 'true'}
    data     = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    analysis = response.json()
    #print analysis

    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    #print word_infos
    #word_info[0]['text']
    json_words = []
    for x in word_infos :
        json_words.append(x[u'text'])
        

    js = json.dumps(json_words)
    resp = Response(js,status=200,mimetype='application/json')

    return resp

if __name__ == '__main__':
   app.run()