'''
The smart meter acts as the receiver of electricity from the substation.
It calcualtes the amount of electricity used by the connected household and
sends this data to the substation.
'''

import random

class SmartMeter(object):

    '''
    The Smart Meter class is used to calculate the amount of electricity used by a household
    '''

    def __init__(self, usage):

        '''
        The initialiser for the meter class

        Args:
            usage: the amount of electricity used at a given time by the connected household
        '''

        self._usage = usage

    def updateUsage(self):

        '''
        Returns the amount of electricity used by the connected household

        Returns:
            usage: the amount of electricity used by the connected household
        '''

        return self.calculateUsage(self._usage)

    def calculateUsage(self):

        '''
        Calculates the amount of electricity used by the connected households
        (For now I will randomly generate a number between 3500 and 6000 - average daily usage)
        '''

        self._usage = random.randint(3500, 6000)


        

  



