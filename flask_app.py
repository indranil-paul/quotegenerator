from calendar import c
import os
from urllib import request
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from random import randrange
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
## =======================[ import section ended ]===============================

# Global declarations
QUOTES = None
QOUTE_FILENAME = 'quotes.csv'
BASEDIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)


## This function will be executed before any request comes
@app.before_request
def prepare_sentiment_quote_stash():
    try:
        global QUOTES
        
        # Load the quote csv
        QUOTES = pd.read_csv(os.path.join(BASEDIR, 'static', 'data', QOUTE_FILENAME))
        
        sia = SentimentIntensityAnalyzer()
        
        # Generate polarity scores or sentiment scores for each qoutes
        all_compounds = []
        for sentence in QUOTES['quote']:
            polarity_score = sia.polarity_scores(sentence)
            for val in sorted(polarity_score):
                if val == 'compound':
                    all_compounds.append(val)
                    
        # Add sentiment score in data as a new column
        QUOTES['sentiment_score'] = all_compounds
        
        # Create ladder index
        QUOTES = QUOTES.sort_values('sentiment_srore')        
        QUOTES['index'] = [idx for idx in range(0, len(QUOTES))]
        
    except Exception as e:
        pass
    
    
def get_a_quote(direction = None, current_index = None, max_index_val = 0):
    rnd_index_val = randrange(max_index_val)        
    darker = None
    brighter = None
    
    if current_index is None:
        brighter = rnd_index_val
    
    if direction == 'brighter':
        brighter = current_index
    else:
        darker = current_index
        
    if darker is not None:
        current_index = int(darker)        
        if current_index > 0:
            # Try a lesser value than current one
            actual_index = randrange(0, current_index)
        else:
            # Already at lowest point, so assign a new random one
            actual_index = rnd_index_val
        
    elif brighter is not None:
        current_index = int(brighter)
        if brighter < max_index_val - 1:
            # Try a higher value than current one
            actual_index = randrange(current_index, max_index_val)
        else:
            # Already at higest point, so assign a new random one
            actual_index = rnd_index_val
    else:
        # Grab a random value
        actual_index = rnd_index_val
        
    return actual_index


@app.route("/")
def quote_me():
    try:
        qoutes_stash_temp = QUOTES.copy()
        max_index_val = np.max(qoutes_stash_temp['index'].values)
        rnd_index_val = randrange(max_index_val)
        
        darker = request.args.get("darker")
        brighter = request.args.get("brighter")
        
        if darker is not None:
            try:
                cur_index = int(darker)
            except ValueError:
                cur_index = randrange(max_index_val)
            
            new_index_val = get_a_quote(direction='darker', current_index=cur_index, max_index_val=max_index_val)                        
        elif brighter is not None:
            try:
                cur_index = int(brighter)
            except ValueError:
                cur_index = randrange(max_index_val)
            
            new_index_val = get_a_quote(direction='brighter', current_index=cur_index, max_index_val=max_index_val)                        
        else:
            new_index_val = randrange(max_index_val)
        
        the_quote = qoutes_stash_temp.iloc[new_index_val]
        
        quote = the_quote['quote']
        author = the_quote['author']
        cur_id = the_quote['index']
        
        return render_template("quote.html", quote=quote, author=author, cur_id=cur_id)
    
    except Exception as e:
        pass


## This route can be used to check whether the application is responding or not
@app.route('/health')
def health():
    return f"{os.path.basename(BASEDIR).upper()} says: I am fine!"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
