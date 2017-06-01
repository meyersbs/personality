import csv

from .constants import CY, MA, YE, GR, OR, RE, XX, VERBS_PATH

def clean_list(list_to_clean):
    return [v for v in list_to_clean if v != '']

#### FROM github.com/andymeneely/sira-nlp/app/lib/helpers.py#L95-L113
def get_verbs():
    """
    Return the contents of verbs file pointed to by the filepath argument as a
    dictionary in which the key is the conjugate of a verb and the value is
    uninflected verb form of the conjugate verb.
    For example, {'scolded': 'scold', 'scolding': 'scold'}
    Adapted from code provided in NodeBox:
    https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
    """
    verbs = dict()
    with open(VERBS_PATH) as file:
        reader = csv.reader(file)
        for row in reader:
            for verb in row[1:]:
                verbs[verb] = row[0]

    return verbs

def print_warning(label, sent, test, train):
    out  = "{:s}\n==== WARNING: Invalid Prediction ===={:s}".format(RE, XX)
    out += "  Label:\t{:s}".format(label)
    out += "  Sentence:\t{:s}".format(sent)
    out += "{:s}  Expected:\t{:s}{:s}".format(GR, test, XX)
    out += "{:s}  Predicted:\t{:s}{:s}".format(YE, train, XX)
    out += "{:s}\n=====================================\n".format(RE)

    print(out)

def print_preds(preds, title):
    out  = "\n============================"
    out += "\n" + title
    out += "{:s}\n {:=<27s}{:s}".format(CY, "EXTRAVERSION: ", XX)
    out += "\n   {: >13s} {: >11s}".format("shy", "extraverted")
    out += "\n  %{: >13f} {: >11f}".format(preds['eRatio_n'], preds['eRatio_y'])
    out += "{:s}\n {:=<27s}{:s}".format(MA, "NEUROTICISM: ", XX)
    out += "\n   {: >13s} {: >11s}".format("secure", "neurotic")
    out += "\n  %{: >13f} {: >11f}".format(preds['nRatio_n'], preds['nRatio_y'])
    out += "{:s}\n {:=<27s}{:s}".format(YE, "AGREEABLENESS: ", XX)
    out += "\n   {: >13s} {: >11s}".format("uncooperative", "friendly")
    out += "\n  %{: >13f} {: >11f}".format(preds['aRatio_n'], preds['aRatio_y'])
    out += "{:s}\n {:=<27s}{:s}".format(GR, "CONSCIENTIOUSNESS: ", XX)
    out += "\n   {: >13s} {: >11s}".format("careless", "precise")
    out += "\n  %{: >13f} {: >11f}".format(preds['cRatio_n'], preds['cRatio_y'])
    out += "{:s}\n {:=<27s}{:s}".format(OR, "OPENNESS: ", XX)
    out += "\n   {: >13s} {: >11s}".format("unimaginative", "insightful")
    out += "\n  %{: >13f} {: >11f}".format(preds['oRatio_n'], preds['oRatio_y'])
    out += "\n============================"

    print(out)

