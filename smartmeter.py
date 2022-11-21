'''
The smart meter acts as the receiver of electricity from the substation.
It calcualtes the amount of electricity used by the connected household and
sends this data to the substation.
'''
import sqlite3 as sl
connect = sl.connect('total.db')
cursor = connect.cursor()

class SmartMeter(object):

    '''
    The Smart Meter class is used to calculate the amount of electricity used by a household
    '''

    def __init__(self):

        '''
        The initialiser for the meter class

        Args:
            received: the amount of electricity received from the substation
            usage: the amount of electricity used by the connected household
            time: the time at which the usage was calculated
        '''

        self._received = 0
        self._usage = 0
        self._time = 0

    def updateUsage(self):

        '''
        Returns the amount of electricity used by the connected household

        Returns:
            usage: the amount of electricity used by the connected household
        '''

        return self.calculateUsage()

    def calculateUsage(self):

        '''
        Calculates the amount of electricity used by the connected households by 
        reading the total consumption and number of smart meters at a given time
        '''

        with connect:

            query = f"SELECT time, usage FROM ussage WHERE time = {self._time}"

            self._time += 0.25

            cursor.execute(query)

            data = cursor.fetchall()
            
            for value in data:
                self._usage = value[1]
                return self._usage

if __name__ == "__main__":
    meter = SmartMeter()


        

  



