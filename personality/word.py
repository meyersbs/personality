__all__ = ['Word']

from .constants import CY, MA, YE, GR, OR, XX

class Word(object):
    @classmethod
    def init(cls, word, word_data=None):
        """
        Given a word (str) and it's associated data (list), create a new 'Word'
        object with 24 fields:
            word     : the given word
            count    : the number of occurences of this word within the dataset
            eFreq_n  : the number of times this word is associated with a status
                       labelled as 'shy'
            eFreq_y  : the number of times this word is associated with a status
                       labelled as 'extraverted'
            nFreq_n  : the number of times this word is associated with a status
                       labelled as 'secure'
            nFreq_y  : the number of times this word is associated with a status
                       labelled as 'neurotic'
            aFreq_n  : the number of times this word is associated with a status
                       labelled as 'uncooperative'
            aFreq_y  : the number of times this word is associated with a status
                       labelled as 'friendly'
            cFreq_n  : the number of times this word is associated with a status
                       labelled as 'careless'
            cFreq_y  : the number of times this word is associated with a status
                       labelled as 'precise'
            oFreq_n  : the number of times this word is associated with a status
                       labelled as 'unimaginative'
            oFreq_y  : the number of times this word is associated with a status
                       labelled as 'insightful'
            eRatio_n : the ratio of eFreq_n / count
            eRatio_y : the ratio of eFreq_y / count
            nRatio_n : the ratio of nFreq_n / count
            nRatio_y : the ratio of nFreq_y / count
            aRatio_n : the ratio of aFreq_n / count
            aRatio_y : the ratio of aFreq_y / count
            cRatio_n : the ratio of cFreq_n / count
            cRatio_y : the ratio of cFreq_y / count
            oRatio_n : the ratio of oFreq_n / count
            oRatio_y : the ratio of oFreq_y / count
        """
        instance = cls()

        instance.word = word

        instance.count = 1

        if instance.word == '([{<NULL>}])':
            instance.eFreq_n = 0
            instance.eFreq_y = 0
            instance.nFreq_n = 0
            instance.nFreq_y = 0
            instance.aFreq_n = 0
            instance.aFreq_y = 0
            instance.cFreq_n = 0
            instance.cFreq_y = 0
            instance.oFreq_n = 0
            instance.oFreq_y = 0
        else:
            if word_data[0] == 'n':
                instance.eFreq_n = 1 # shy
                instance.eFreq_y = 0 # extravert
            else:
                instance.eFreq_n = 0 # shy
                instance.eFreq_y = 1 # extravert
            if word_data[1] == 'n':
                instance.nFreq_n = 1 # secure
                instance.nFreq_y = 0 # neurotic
            else:
                instance.nFreq_n = 0 # secure
                instance.nFreq_y = 1 # neurotic
            if word_data[2] == 'n':
                instance.aFreq_n = 1 # uncooperative
                instance.aFreq_y = 0 # friendly
            else:
                instance.aFreq_n = 0 # uncooperative
                instance.aFreq_y = 1 # friendly
            if word_data[3] == 'n':
                instance.cFreq_n = 1 # careless
                instance.cFreq_y = 0 # precise
            else:
                instance.cFreq_n = 0 # careless
                instance.cFreq_y = 1 # precise
            if word_data[4] == 'n':
                instance.oFreq_n = 1 # unimaginative
                instance.oFreq_y = 0 # insightful
            else:
                instance.oFreq_n = 0 # unimaginative
                instance.oFreq_y = 1 # insightful


        instance.eRatio_n = float( instance.eFreq_n / instance.count )
        instance.eRatio_y = float( instance.eFreq_y / instance.count )
        instance.nRatio_n = float( instance.nFreq_n / instance.count )
        instance.nRatio_y = float( instance.nFreq_y / instance.count )
        instance.aRatio_n = float( instance.aFreq_n / instance.count )
        instance.aRatio_y = float( instance.aFreq_y / instance.count )
        instance.cRatio_n = float( instance.cFreq_n / instance.count )
        instance.cRatio_y = float( instance.cFreq_y / instance.count )
        instance.oRatio_n = float( instance.oFreq_n / instance.count )
        instance.oRatio_y = float( instance.oFreq_y / instance.count )

        #print(instance)
        return instance


    def update_freqs(self, updates=['n','n','n','n','n']):
        self.count += 1
        if updates[0] == 'n':
            self.eFreq_n += 1 # shy
        else:
            self.eFreq_y += 1 # extravert
        if updates[1] == 'n':
            self.nFreq_n += 1 # secure
        else:
            self.nFreq_y += 1 # neurotic
        if updates[2] == 'n':
            self.aFreq_n += 1 # uncooperative
        else:
            self.aFreq_y += 1 # friendly
        if updates[3] == 'n':
            self.cFreq_n += 1 # careless
        else:
            self.cFreq_y += 1 # precise
        if updates[4] == 'n':
            self.oFreq_n += 1 # unimaginative
        else:
            self.oFreq_y += 1 # insightful

        self.update_ratios()
        #print(self)
        return True


    def update_ratios(self):
        self.eRatio_n = float( self.eFreq_n / self.count )
        self.eRatio_y = float( self.eFreq_y / self.count )
        self.nRatio_n = float( self.nFreq_n / self.count )
        self.nRatio_y = float( self.nFreq_y / self.count )
        self.aRatio_n = float( self.aFreq_n / self.count )
        self.aRatio_y = float( self.aFreq_y / self.count )
        self.cRatio_n = float( self.cFreq_n / self.count )
        self.cRatio_y = float( self.cFreq_y / self.count )
        self.oRatio_n = float( self.oFreq_n / self.count )
        self.oRatio_y = float( self.oFreq_y / self.count )


    def __str__(self):
        out  = "\n============================="
        out += "\nWORD: " + self.word
        out += "{:s}\n  {:=<27s}{:s}".format(CY, "EXTRAVERSION: ", XX)
        out += "\n    {: >13s} {: >11s}".format("shy", "extraverted")
        out += "\n  # {: >13d} {: >11d}".format(self.eFreq_n, self.eFreq_y)
        out += "\n  % {: >13f} {: >11f}".format(self.eRatio_n, self.eRatio_y)
        out += "{:s}\n  {:=<27s}{:s}".format(MA, "NEUROTICISM: ", XX)
        out += "\n    {: >13s} {: >11s}".format("secure", "neurotic")
        out += "\n  # {: >13d} {: >11d}".format(self.nFreq_n, self.nFreq_y)
        out += "\n  % {: >13f} {: >11f}".format(self.nRatio_n, self.nRatio_y)
        out += "{:s}\n  {:=<27s}{:s}".format(YE, "AGREEABLENESS: ", XX)
        out += "\n    {: >13s} {: >11s}".format("uncooperative", "friendly")
        out += "\n  # {: >13d} {: >11d}".format(self.aFreq_n, self.aFreq_y)
        out += "\n  % {: >13f} {: >11f}".format(self.aRatio_n, self.aRatio_y)
        out += "{:s}\n  {:=<27s}{:s}".format(GR, "CONSCIENTIOUSNESS: ", XX)
        out += "\n    {: >13s} {: >11s}".format("careless", "precise")
        out += "\n  # {: >13d} {: >11d}".format(self.cFreq_n, self.cFreq_y)
        out += "\n  % {: >13f} {: >11f}".format(self.cRatio_n, self.cRatio_y)
        out += "{:s}\n  {:=<27s}{:s}".format(OR, "OPENNESS: ", XX)
        out += "\n    {: >13s} {: >11s}".format("unimaginative", "insightful")
        out += "\n  # {: >13d} {: >11d}".format(self.oFreq_n, self.oFreq_y)
        out += "\n  % {: >13f} {: >11f}".format(self.oRatio_n, self.oRatio_y)
        out += "\n============================="
        return out
