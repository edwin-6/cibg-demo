pip install -U pip setuptools wheel
pip install -U spacy[transformers,lookups]
pip install -U scikit-learn
pip install -U idna==2.8

python -m spacy project clone pipelines/ner_demo
python -m spacy project run split
python -m use_zipcodes_model.py
