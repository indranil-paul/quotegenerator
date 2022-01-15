import os
import pandas as pd
import numpy as np
from flask import Flask

import nltk

## Download the vader_lexicon algorithm
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

## =======================[ import section ended ]===============================

# Global declarations
BASEDIR = os.path.dirname(os.path.abspath(__file__))
QUOTES= None


app = Flask(__name__)


## This route can be used to check whether the application is responding or not
@app.route('/health')
def health():
    return f"{os.path.basename(BASEDIR).upper()} says: I am fine!"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
