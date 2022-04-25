from flask import Flask

import urllib.request
import json


app = Flask(__name__)

def get_prediction(comment):
    body = {'Comment': comment}

    myurl = "http://0.0.0.0:5000/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return response.json()['predictions']
#comment = 'Writing a captivating and thoughtful speech requires one to select a good topic, research it thoroughly and formation of individual opinions to express on the same. School students are usually asked to speak on a contemporary topic in order to help them become good public speakers as'
#get_prediction(comment)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)