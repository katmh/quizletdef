import os
import json
import requests
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from flask import Flask, render_template, request
from apidata import client_ID

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class TermsForm(FlaskForm):
    terms = TextAreaField('Terms')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TermsForm()
    if request.method == 'POST':
        terms = request.form.get('terms').splitlines()

        r = requests.get('https://api.quizlet.com/2.0/sets/10451368', params=client_ID)

        parsed_json = json.loads(r.content)         

        terms_defs = []

        for term in terms:
            for quizlet_term in parsed_json['terms']:
                if quizlet_term['term'] == term:
                    terms_defs.append( term + ' - ' + quizlet_term['definition'] )

        return render_template('output.html', output=terms_defs)
    else:
        return render_template('index.html', form=form)