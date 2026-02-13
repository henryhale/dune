.ONESHELL:

setup:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('stopwords')"
	./venv/bin/python -m src.preprocess

train:
	./venv/bin/python -m src.train --output-onnx=True

serve:
	./venv/bin/python app.py --debug=True

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