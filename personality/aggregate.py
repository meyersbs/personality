import csv
import _pickle
import sys
import random
import re

from . import constants, status, word

def _clean(word):
    new_word = re.sub(r"[\.!?,:;@%$\^\)\(\]\[\{\}\*=\+\<\>\'\"#]+", '', word)
    return new_word.replace('\r', '\n')

def aggregate_train_test(train_size, data=constants.DATASET_CLEANED_PATH):
    with open(data, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        statuses = list(csv_reader)
        statuses = statuses[1:] # skip the header row
        size = len(statuses)

    train_words, test_words = dict(), dict()
    train_size = int(size*train_size)

    random.shuffle(statuses)

    for i in range(0, train_size):
        status = statuses[i]
        for w in re.split(r'[\s_\-]+', _clean(status[0].lower())):
            if _clean(w) not in train_words.keys():
                train_words[_clean(w)] = word.Word.init(_clean(w), status[6:])
            else:
                train_words[_clean(w)].update_freqs(status[6:])

    for i in range(train_size, size):
        status = statuses[i]
        for w in re.split(r'[\s_\-]+', _clean(status[0].lower())):
            if _clean(w) not in test_words.keys():
                test_words[_clean(w)] = word.Word.init(_clean(w), status[6:])
            else:
                test_words[_clean(w)].update_freqs(status[6:])

    with open(constants.AGGREGATE_TRAINING, 'wb') as out_file:
        _pickle.dump(train_words, out_file)
    with open(constants.AGGREGATE_TESTING, 'wb') as out_file:
        _pickle.dump(test_words, out_file)
    stats = []
    with open(constants.AGGREGATE_TESTING_STATUSES, 'w') as out_file:
        csv_writer = csv.writer(out_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for status in statuses:
            csv_writer.writerow([status[0]])
            stats.append(status[0])
    return train_words, test_words, stats

def aggregate_data(data=constants.DATASET_CLEANED_PATH):
    with open(data, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader, None) # skip the header row

        words = dict()
        # for each line in the csv file
        for status in csv_reader:
            # for each word in the status
            for w in re.split(r'[\s_\-]+', _clean(status[0].lower())):
                # create a Word object if we don't have one
                if _clean(w) not in words.keys():
                    words[_clean(w)] = word.Word.init(_clean(w), status[6:])
                # update the Word object if it exists
                else:
                    words[_clean(w)].update_freqs(status[6:])

    with open(constants.AGGREGATE_INFO_FILE, 'wb') as out_file:
        _pickle.dump(words, out_file)
    return words
