import nltk
import os

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from . import constants, helpers

#### FROM github.com/andymeneely/sira-nlp/app/lib/nlp/postagger.py
class PosTagger(object):
    """
    Given a list of tokens, return a list of tuples of the form:
    (token, part-of-speech-tag)
    """
    def __init__(self, tokens):
        """ Constructor. """
        self.tokens = tokens

    def execute(self):
        """
        Given a list of tokens, return a list of tuples of the form:
        (token, part-of-speech-tag)
        """
        return nltk.pos_tag(self.tokens)

#### FROM github.com/andymeneely/sira-nlp/app/lib/nlp/lemmatizer.py
VERBS = helpers.get_verbs()
WORDNET_POS = {
        'N': wordnet.NOUN, 'V': wordnet.VERB, 'J': wordnet.ADJ, 'R': wordnet.ADV
    }
MAP = {
        "'m": 'am', "'ll": 'will', "n't": 'not', "'ve": 'have', "'re": 'are'
    }

lemmatizer = WordNetLemmatizer()

class Lemmatizer(object):
    """ Interface. """
    def __init__(self, tokens):
        """ Constructor. """
        self.tokens = tokens

    def execute(self):
        """ Raises NotImplementedError. """
        raise NotImplementedError("Lemmatizer is an abstract class. In must "
                                  "be implemented by another class. Try using "
                                  "the NLTKLemmatizer.")

def fix(token, lemma, prev=None, next=None):
    """
    Attempts to fix lemmatization errors with hardcoded rules.
    """
    if not token and not lemma and not prev and not next:
        raise ValueError("Recieved invalid input to lemmatizer.fix()")
    elif token.lower() == "ca":
        if next and next[0] and next[0].lower() == "n't":
            return "can"
        else:
            return lemma.lower()
    elif token.lower() == "as":
        return "as"
    elif token.lower() == "left":
        if prev and prev[1] == wordnet.VERB:
            return "leave"
        else:
            return lemma.lower()
    elif token in MAP:
        return MAP[token]
    elif lemma in VERBS:
        return VERBS[lemma]
    elif token in VERBS:
        return VERBS[token]
    else:
        return lemma.lower()

class NLTKLemmatizer(Lemmatizer):
    """ Implements Lemmatizer. """
    def __init__(self, tokens):
        """ Constructor. """
        super().__init__(tokens)

    def execute(self):
        """ Return a list of all tokens within the specified string. """
        lemmas = []

        #print(self.tokens)
        tokens = [
                (t, WORDNET_POS.get(p[0], wordnet.NOUN))
                for (t, p) in PosTagger(self.tokens).execute()
            ]

        for (i, (token, pos)) in enumerate(tokens):
            lemma = lemmatizer.lemmatize(token, pos)
            prev = None if i == 0 else tokens[i - 1]
            next = None if i == len(tokens) - 1 else tokens[i + 1]
            lemmas.append(fix(token, lemma, prev, next))

        return lemmas

