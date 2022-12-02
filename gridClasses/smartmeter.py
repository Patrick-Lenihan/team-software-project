'''
The smart meter acts as the receiver of electricity from the substation.
It calcualtes the amount of electricity used by the connected household and
sends this data to the substation.
'''
import sqlite3 as sl
connect = sl.connect('app.db')
cursor = connect.cursor()

class SmartMeter(object):

    '''
    The Smart Meter class is used to calculate the amount of electricity used by a household
    '''

    def __init__(self):

        '''
        The initialiser for the meter class
        Args:
            usage: the amount of electricity used by the connected household
            time: the time at which the usage was calculated
        '''

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
        Returns the amount of electricity used by the connected household by
        reading the value from the database
        '''

        with connect:

            query = f"SELECT decTime, usage FROM usage WHERE decTime = {self._time}"

            self._time += 0.25

            cursor.execute(query)

            data = cursor.fetchall()
            

            for value in data:
                self._usage = value[1]
                return self._usage
