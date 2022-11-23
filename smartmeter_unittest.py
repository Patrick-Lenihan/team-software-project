import unittest
import sqlite3 as sl
from smartmeter import SmartMeter

class TestSmartMeter(unittest.TestCase):

    def setup(self):

        '''
        Setup run at the beginning of each test to ensure clean database for each test.
        Can be called again where the database is changed and more tests are required.
        'use' values in the table are unique in this example for tracing bugs and 
        to avoid false positive tests.
        '''

        connect = sl.connect('total.db')
        cursor = connect.cursor()

        # Create a table to store the time and total usage
        with connect:

            # Create the table
            cursor.execute('CREATE TABLE IF NOT EXISTS total_usage (ID INTEGER PRIMARY KEY, time FLOAT, usage INT, num_meters INT)')

            # Open the file 
            with open('weeklyUsage.txt', 'r') as f:

                # Read the file and separate the time and usage
                for line in f:
                            
                    # Split the line into three
                    time, usage, num_meters = line.split()
                    
                    # Insert the data into the table
                    cursor.execute('''INSERT INTO total_usage(time, usage, num_meters) VALUES(?,?,?);''', (time, usage, num_meters))

    
        self.smartmeter = SmartMeter()

    def test_calculate_usage(self):
        self.setup()
        for i in range(10):
            usage = self.smartmeter.calculateUsage()
            print(usage)

if __name__ == "__main__":
    unittest.main()
