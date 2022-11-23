import unittest
import sqlite3 as sl
import csv
from smartmeter import SmartMeter

class TestSmartMeter(unittest.TestCase):

    def test_calculate_usage(self):

        '''
        Setup run at the beginning of each test to ensure clean database for each test.
        Can be called again where the database is changed and more tests are required.
        'use' values in the table are unique in this example for tracing bugs and 
        to avoid false positive tests.
        '''

        # Write unit test for getSmartMeterUsage
        conn = sl.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE usage")
        cursor.execute("CREATE TABLE usage (decTime TEXT, usage INTEGER)")
        cursor.execute("INSERT INTO usage VALUES (0,2345432)")
        conn.commit()

        # Get smart meter usage from database
        meter = SmartMeter()
        meter.calculateUsage()
    
        # Check if usage is correct
        self.assertEqual(meter._usage, 2345432, 'smart meter did not calculate total usage correctly')

    def test_update_usage(self):

        # Test update usage
        conn = sl.connect('app.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE usage")
        cursor.execute("CREATE TABLE usage (decTime TEXT, usage INTEGER)")
        cursor.execute("INSERT INTO usage VALUES (0,2345432)")
        conn.commit()

        # Get smart meter usage from database
        meter = SmartMeter()
        meter.updateUsage()

        # Check if usage is correct
        self.assertEqual(meter._usage, 2345432, 'smart meter did not calculate total usage correctly')



if __name__ == "__main__":
    unittest.main()