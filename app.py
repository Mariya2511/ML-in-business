import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

app = Flask(__name__)
model = None


handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)
	return model

modelpath = "my_flask_app/pipeline.dill"
load_model(modelpath)
@app.route("/", methods=["GET"])
def general():
	return """Welcome to prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	data = {"success": False, "predictions": ''}
	comment = ""
	request_json = flask.request.get_json()
	if (flask.request.method == "POST"):
		if request_json["comment"]:
			comment = request_json["comment"]
		logger.info(f'Data: comment={comment}')
		try:
			preds = model.predict_proba(pd.DataFrame({"comment": [comment]}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True
	# return the data dictionary as a JSON response
	return  flask.jsonify(data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')