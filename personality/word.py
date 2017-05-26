__all__ = ['Word']


class Word(object):
    @classmethod
    def init(cls, word, word_data):
        instance = cls()

        instance.word = word

        instance.count = 1

        instance.eFreq = 0 if word_data[0] == 'n' else 1
        instance.nFreq = 0 if word_data[1] == 'n' else 1
        instance.aFreq = 0 if word_data[2] == 'n' else 1
        instance.cFreq = 0 if word_data[3] == 'n' else 1
        instance.oFreq = 0 if word_data[4] == 'n' else 1

        instance.eRatio = float( instance.eFreq / instance.count )
        instance.nRatio = float( instance.nFreq / instance.count )
        instance.aRatio = float( instance.aFreq / instance.count )
        instance.cRatio = float( instance.cFreq / instance.count )
        instance.oRatio = float( instance.oFreq / instance.count )

        #print(instance)
        return instance

    def update_freqs(self, updates=['n','n','n','n','n']):
        self.count += 1
        self.eFreq += 0 if updates[0] == 'n' else 1
        self.nFreq += 0 if updates[1] == 'n' else 1
        self.aFreq += 0 if updates[2] == 'n' else 1
        self.cFreq += 0 if updates[3] == 'n' else 1
        self.oFreq += 0 if updates[4] == 'n' else 1

        self.update_ratios()
        print(self)
        return True

    def update_ratios(self):
        self.eRatio = float( self.eFreq / self.count )
        self.nRatio = float( self.nFreq / self.count )
        self.aRatio = float( self.aFreq / self.count )
        self.cRatio = float( self.cFreq / self.count )
        self.oRatio = float( self.oFreq / self.count )

    def __str__(self):
        out = ("\n=====\nWORD: " + self.word +
               "\n  Extraversion:\n" +
               "    #: " + str(self.eFreq) + "\n" +
               "    %: " + str(self.eRatio) +
               "\n  Neuroticism:\n" +
               "    #: " + str(self.nFreq) + "\n" +
               "    %: " + str(self.nRatio) +
               "\n  Agreeableness:\n" +
               "    #: " + str(self.aFreq) + "\n" +
               "    %: " + str(self.aRatio) +
               "\n  Conscientiousness:\n" +
               "    #: " + str(self.cFreq) + "\n" +
               "    %: " + str(self.cRatio) +
               "\n  Openness:\n" +
               "    #: " + str(self.oFreq) + "\n" +
               "    %: " + str(self.oRatio) +
               "\n=====")
        return out


