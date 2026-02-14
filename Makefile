# makefile for local development only

.ONESHELL:

setup:
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('stopwords')"
	python -m src.preprocess

train:
	python -m src.train --output-onnx=True

serve:
	python app.py --debug=True

browser-setup: train
	cp models/pipeline.onnx app/public/model/
	cp models/classes.json app/public/model/
	cd app
	pnpm install

browser-build: browser-setup
	cd app
	pnpm run browser:build

clean:
	rm -rf app/dist/
	rm app/public/model/pipeline.onnx
	rm app/public/model/classes.json
	rm models/pipeline.onnx
	rm models/pipeline.joblib
	rm models/classes.json