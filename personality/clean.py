import csv
import os

from . import constants

HEADER = [
        # New Label     # Old Label
        "text",         # STATUS : a Facebook status
        "xScore",       # sEXT   : numerical Extraversion score
        "nScore",       # sNEU   : numerical Neuroticism score
        "aScore",       # sAGR   : numerical Agreeableness score
        "cScore",       # sCON   : numerical Conscientiousness score
        "oScore",       # sOPN   : numerical Openness score
        "xBin",         # cEXT   : binary Extraversion flag
        "nBin",         # cNEU   : binary Neuroticism flag
        "aBin",         # cAGR   : binary Agreeableness flag
        "cBin",         # cCON   : binary Conscientiousness flag
        "oBin"          # cOPN   : binary Openness flag
    ]

def clean_data(data_in=constants.DATASET_ORIGINAL_PATH,
               data_out=constants.DATASET_CLEANED_PATH):

    with open(data_in, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None) # skip the header row

        with open(data_out, "w") as outfile:
            writer = csv.writer(outfile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)

            for row in reader:
                print(row)
                writer.writerow(row[1:12])


if __name__=="__main__":
    clean_data()
