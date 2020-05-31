from flask import Flask, render_template, request
from main import create_abstract
import tensorflow as tf
from tensorflow import keras
import pandas as pd

# Create the application.
app = Flask(__name__)

# Define global variables for model & dataframe
title_model = None
abstract_model = None
dataframe = None

def load_all():
    global title_model, abstract_model, dataframe
    title_model = tf.keras.models.load_model('data/title.h5', compile=False)
    abstract_model = tf.keras.models.load_model('data/abstract.h5', compile=False)
    dataframe = pd.read_csv('data/ArXiv.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abstract',methods=['GET', 'POST'])
def abstract():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            keyword = request.form['keyword']
            method = request.form['subject']
            title, body = create_abstract(keyword, method, dataframe, title_model, abstract_model)
            results = {'title':title, 'body':body, 'keywords':'keywords: ' + keyword}
        except IndexError:
            error_msg = "Unable to get keyword(s). Please make sure it's about physics/math/computer science/chemistry and try again."
            if error_msg not in errors:
                errors.append(error_msg)
    return render_template('abstract.html',errors=errors, results=results)

if __name__ == '__main__':
    app.debug=True
    load_all()
    app.run()
