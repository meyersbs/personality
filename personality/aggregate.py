import csv

from . import constants, status, word

def aggregate_data(data=constants.DATASET_CLEANED_PATH):
    with open(data, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader, None) # skip the header row

        words = dict()
        # for each line in the csv file
        for status in csv_reader:
            # for each word in the status
            for w in status[0].lower().split():
                # create a Word object if we don't have one
                if w not in words.keys():
                    words[w] = word.Word.init(w, status[6:])
                # update the Word object if it exists
                else:
                    words[w].update_freqs(status[6:])
