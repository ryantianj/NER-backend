# ML-backend

This application uses Named Entity Recognition (NER) for machine learning on texts.<br/>
It aims to be a general purpose application for users to build and test text related machine learning models
<br/>
It utilises [Spacy](https://spacy.io/api), an open source python machine learning library for text classification

- A blank model is used as a template (train from scratch).
- This application can be used for text CLASSIFICATION problems.
- In the future, if different types of machine learning models are required, the code used to train may need to be expanded upon. Specifically add a different pipeline to the model.
- You can train and test your own models
- The sample model called "test" uses 4 tags: PRODUCT, PRICE, MEMBER, UPC
- You can run the server and test the endpoint http://localhost:5000/test
- Required request keys can be found in the code in app.py

## Development environment

Python3 virtual environment required: Refer to Flask environment instructions.
<br/>
You will also need to have pip installed (python3 package manager).

### Flask environment

Instructions to set up flask:
<br/>
Commands are ran in the **working directory**.

1. Have python3 installed on your computer
2. Create a virtual environment `python3 -m venv <name of environment>`
3. Activate the environment `. <name of environment>/bin/activate`. If you do not do this, some python packages may be missing
4. Install flask if it is already not installed `pip install Flask`
5. You may need to set the entry point `export FLASK_APP=app.py` for this app
6. Start the app by using `python app.py`
7. To deactivate the environment (after you're done developing): `deactivate`
8. Server will be runnning on `http://localhost:5000` unless otherwise specified by the developer / operating system

Full instructions [here](https://phoenixnap.com/kb/install-flask) if the above instructions do not suffice.

Before the app can run, you need to do the following: <br/>
To install all required packages: `pip install -r requirements.txt`
<br/>
To update required packages (if you added a new package to the project): `pip freeze > requirements.txt`

## Developer notes

Comments are placed throughout the code for clarity.
<br/>
Also remember to update .gitignore to ignore commiting the virtual environment folder

### app.py

Entry point of the application. Uses flask (backend framework for python).
<br/>
Waitress is used for the server (Something like Node Express).
<br/>
Sample training data is commented out. This format is required by Spacy.

### train.py

All of the machine learning logic is encapsulated in this file, including training and testing logic. Trained models are saved locally in the `/models` directory.
<br/>
Models that are going to be used for production can be used in a similar fashion as the "test" function in the file

### service.py

This file contains logic to upload models / interact with the databases. At the point of documentation, such logic is not implemented yet.

### Other files and folders

1. **pycache** is used by python virtual environment for caching - This will be created after you run the virtual environment for the first time
2. `<name of environment>` as mentioned in the Flask instructions. This folder will hold the data for the python virtual environment (venv)
3. **models** is used for storing models locally

## Machine Learning Notes

For best results, use a realisitic set of training data

- Order of data matters (e.g. $1000 Samsung Galaxy S3 vs Samsung Galaxy S3 $1000)
- If order matters, train the model with ALL possible orders (e.g. if 4 labels, train 4! = 24 different combinations for the best results)
- Give a diverse set of training data - include edges cases if possible (e.g. If model is being trained to detect product name and price, and if product name contains numbers, includes those numbers as well)

When testing the model, if the model gives a wrong output, take that output and feed the correct version back to the model

- e.g. model classifies 'Samsung Galaxy S3 $1000' as PRODUCT, which is wrong as '$1000' is not part of PRODUCT
- In such a case, properly feed the model by including in the training dataset: '$1000' -> PRICE and 'Samsung Galaxy S3' -> PRODUCT
- This method is quite effective in improving the accuracy of the model

Since this application is used for text classification, make sure the input text is more or less PROPER English

- Remove underscores, punctuations, other special non-english characters to improve accuracy of the model
- Avoid abbreviations if possible

Make the model train itself:

- Use the output of the production model to train the model again
- Improves the model
- Human intervention required: Ensure that the outputs are valid. Training the model with invalid outputs will WORSEN the model.
