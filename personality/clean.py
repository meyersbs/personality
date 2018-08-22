import csv
import os

from . import constants

HEADER = [
        # New Label     # Old Label
        "text",         # STATUS : a Facebook status
        "eBin",         # cEXT   : binary Extraversion flag
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

            author = ""
            text = []
            for row in reader:
                if author == "":
                    author = row[0]
                    text.append(row[1])
                elif author == row[0]:
                    text.append(row[1])
                else:
                    new_row = [" ".join(text), row[7], row[8], row[9], row[10], row[11]]
                    writer.writerow(new_row)
                    author = ""
                    text = []

#                print(row)
#                writer.writerow(row[0:12])


if __name__=="__main__":
    clean_data()
