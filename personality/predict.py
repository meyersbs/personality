import csv
import math
import os
import _pickle
import re

from difflib import get_close_matches

from . import aggregate, helpers, lemmatizer
from . import word as WORD
from .constants import *

DATA = None
DATA_TRAIN = None
DATA_TEST = None

def normalize_ratios(preds):
    """
    Given a well-defined dictionary of personality values, return a dictionary
    with normalized ratios. Ratios are normalized by taking the sum of the '_y'
    and '_n' ratios for a given personality class, and dividing the '_y' and
    '_n' ratios by the sum. This gives us a float between 0 and 1 denoting our
    certainty that the given sentence/text is each respective class.

    Example:
      INPUT: preds = {'eRatio_n': 0.6, 'eRatio_y': 1.4,
                      'nRatio_n': 0.3, 'nRatio_y': 1.7,
                      ...
                     }
      OUTPUT: preds_copy = {'eRatio_n': 0.3, 'eRatio_y': 0.7,
                            'nRatio_n': 0.15, 'nRatio_y': 0.85
                            ...
                           }
    """
    norm_num = preds['eRatio_n'] + preds['eRatio_y']

    preds_copy = preds.copy()
    if norm_num != 0:
        for key in RATIO_KEYS:
            preds_copy[key] = float( preds[key] / norm_num )

    return preds_copy

def predict_sent(sent):
    """
    Given a sentence (str), return a well-formed dictionary of personality
    values where the key is a unique identifier (int), and the value is a list,
    where index 0 is a word (str) and index 1 is its corresponding Word object.

    Prediction follows the following process:
      1) Split the sentence on spaces and underscores.
      2) For each word in the split sentence, if the word is present in the
         'training' data, use the corresponding predictions from the 'training'
         data.
      3) If any of the words in the sentence were not present in the 'training'
         data, find the lemma for each non-present word, and use the
         corresponding predictions from the 'training' data.
      4) If any of the non-presents words had lemmas that were also not present,
         use the library difflib to find the word from the 'training' data that
         most closely matches the non-present word, and use its corresponding
         predictions from the 'training' data.
    """
    global DATA
    preds = {}
    flag = False
    tokens = helpers.clean_list(re.split(r"[\s_\-]+", sent))
    for i, word in enumerate(tokens):
        pred = predict_str(word)
        if pred is None:
            flag = True
        preds[i] = [word, pred]

    if not flag:
        return preds
    else:
        lemmas = lemmatizer.NLTKLemmatizer(
                         helpers.clean_list(re.split(r"[\s_\-]+", sent))
                     ).execute()
        for key, val in preds.items():
            if val[1] is None:
                # Try to make a prediction using the lemma.
                pred = predict_str(lemmas[key])
                if pred is None:
                    # Make a prediction with the closest matching word in the
                    # training data.
                    pred = get_close_matches(val[0], DATA.keys(), 1, 0.0)
                preds[key] = [val[0], predict_str(pred)]
                # This should never happen, but it's a safety net.
                if preds[key][1] is None:
                    preds[key] = [
                            "([{<NULL>}])",
                            WORD.Word.init("([{<NULL>}])", None)
                        ]

        return preds

def aggregate_sent(preds):
    """
    Aggregate the word-level personality predictions into a single dictionary
    with sentence-level predictions. Aggregation is simple: for each key in
    the given (well-formed) prediction dictionary, add its corresponding
    value to respective key in the 'out' dictionary.

    Example:
      INPUT: preds = {0: ['i' , <Word{'eFreq_n': 0.6, 'eFreq_y': 1.4, ...}>,
                      1: ['am', <Word{'eFreq_n': 0.3, 'eFreq_y': 1.7, ...}>,
                      ...
                     }
      OUTPUT: out = {'eFreq_n': 0.9, 'eFreq_y': 3.1, ... }
    """
    count = 0
    out = {
            'eFreq_n': 0, 'eFreq_y': 0, 'eRatio_n': 0, 'eRatio_y': 0,
            'nFreq_n': 0, 'nFreq_y': 0, 'nRatio_n': 0, 'nRatio_y': 0,
            'aFreq_n': 0, 'aFreq_y': 0, 'aRatio_n': 0, 'aRatio_y': 0,
            'cFreq_n': 0, 'cFreq_y': 0, 'cRatio_n': 0, 'cRatio_y': 0,
            'oFreq_n': 0, 'oFreq_y': 0, 'oRatio_n': 0, 'oRatio_y': 0,
            'count': 0
        }
    for key, val in preds.items():
        word = val[1]
        out['count'] += word.count
        out['eFreq_n'] += word.eFreq_n
        out['eFreq_y'] += word.eFreq_y
        out['nFreq_n'] += word.nFreq_n
        out['nFreq_y'] += word.nFreq_y
        out['aFreq_n'] += word.aFreq_n
        out['aFreq_y'] += word.aFreq_y
        out['cFreq_n'] += word.cFreq_n
        out['cFreq_y'] += word.cFreq_y
        out['oFreq_n'] += word.oFreq_n
        out['oFreq_y'] += word.oFreq_y

    if out['count'] != 0:
        for r_key, f_key in zip(RATIO_KEYS, FREQ_KEYS):
            out[r_key] = float( out[f_key] / out['count'] )

    return out

def predict_str(word):
    """
    Helper function to determine whether or not a given word exists within the
    'training' data. If it does, return the corresponding Word object, else
    return None.
    """
    global DATA
    # This should never happen, but it's a safety net.
    if type(word) != list and type(word) != str:
        return None
    # TODO: Figure out why the given 'word' is sometimes a list of length 1.
    elif type(word) == list:
        return DATA[word[0]] if word[0] in DATA.keys() else None
    elif type(word) == str:
        return DATA[word] if word in DATA.keys() else None

def predict_split(train_size):
    if os.path.getsize(TRAIN_PREDICTIONS) == 0:
        print("Splitting Training/Testing Data...")
        _, _, statuses = aggregate.aggregate_train_test(train_size)
        statuses = "\n".join(statuses)
        print("Gathering Features...")
        train_preds = predict(statuses, text_type='str', data=AGGREGATE_TRAINING)
        print("==== DUMPING TRAINING ====")
        with open(TRAIN_PREDICTIONS, 'wb') as f:
            _pickle.dump(train_preds, f)
        test_preds = predict(statuses, text_type='str', data=AGGREGATE_TESTING)
        print("==== DUMPING TESTING ====")
        with open(TEST_PREDICTIONS, 'wb') as f:
            _pickle.dump(test_preds, f)

    with open(TRAIN_PREDICTIONS, 'rb') as f:
        train_preds = _pickle.load(f)
        helpers.print_preds(train_preds, "TRAINING RESULTS")
    with open(TEST_PREDICTIONS, 'rb') as f:
        test_preds = _pickle.load(f)
        helpers.print_preds(test_preds, "TESTING RESULTS")
    print("Reading Testing Data...")
    with open(AGGREGATE_TESTING_STATUSES, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')

        predictions = {}
        print("Collecting Predictions...\n")
        for i, status in enumerate(csv_reader):
            print("\r" + str(i), end="")
            train_pred = predict(status[0], text_type='str', data=AGGREGATE_TRAINING)
            test_pred = predict(status[0], text_type='str', data=AGGREGATE_TESTING)
            predictions[i] = [status[0], pred_to_labels(train_pred), pred_to_labels(test_pred)]

    #sys.exit()
    return predictions

def pred_to_labels(pred):
    labels = {"e": 'n', "n": 'n', "a": 'n', "c": 'n', "o": 'n'}
    if pred['eRatio_y'] > pred['eRatio_n']:
        labels["e"] = 'y'
    if pred['nRatio_y'] > pred['nRatio_n']:
        labels["n"] = 'y'
    if pred['aRatio_y'] > pred['aRatio_n']:
        labels["a"] = 'y'
    if pred['cRatio_y'] > pred['cRatio_n']:
        labels["c"] = 'y'
    if pred['oRatio_y'] > pred['oRatio_n']:
        labels["o"] = 'y'

    #print(labels)
    return labels

def predict(file_in, text_type='file', data=AGGREGATE_INFO_FILE):
    """
    Given a valid filepath, run predict_sent() for each line in the file and
    print out the prediction values for each personality class.
    """
    global DATA
    # Load the 'training' data once
    with open(data, 'rb') as in_file:
        DATA = _pickle.load(in_file)

    if text_type == 'file':
        # Get the raw text from file_in
        with open(file_in, newline='') as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"')
            text = "\n".join(in_file.readlines())
    else:
        text = file_in

    # Aggregate the file-level values
    preds = {'eFreq_n': 0, 'eFreq_y': 0, 'eRatio_n': 0, 'eRatio_y': 0,
             'nFreq_n': 0, 'nFreq_y': 0, 'nRatio_n': 0, 'nRatio_y': 0,
             'aFreq_n': 0, 'aFreq_y': 0, 'aRatio_n': 0, 'aRatio_y': 0,
             'cFreq_n': 0, 'cFreq_y': 0, 'cRatio_n': 0, 'cRatio_y': 0,
             'oFreq_n': 0, 'oFreq_y': 0, 'oRatio_n': 0, 'oRatio_y': 0,
             'count': 0}
    for sent in aggregate._clean(text.lower()).split('\n'):
        if sent != '':
            # Predict & Aggregate sentence-level values
            p = predict_sent(sent)
            aggs = aggregate_sent(p)
            # Update the file-level values
            for key, val in aggs.items():
                preds[key] += val

    preds = normalize_ratios(preds)
    helpers.print_preds(preds, text[0:50])

    return preds
