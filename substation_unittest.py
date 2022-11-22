import unittest
import sqlite3 as sl
from substation import Substation
from smartmeter import SmartMeter
class TestSubstation(unittest.TestCase):

    def test_get_smart_meter_usage(self):
        usage = 2345432
        conn = sl.connect('app.db')
        
        cursor = conn.cursor()
        cursor.execute("DROP TABLE usage")
        cursor.execute("CREATE TABLE usage (decTime TEXT, usage INTEGER)")
        cursor.execute("INSERT INTO usage VALUES (0,2345432)")
        conn.commit()
        meter1 = SmartMeter()
        meter2 = SmartMeter()
        meter3 = SmartMeter()
        meter4 = SmartMeter()
        substation = Substation(0,[meter1, meter2, meter3, meter4])
        substation.getSmartMeterUsage()
        self.assertEqual(substation._usage, usage*(len(substation._users)), 'substation did not calculate total usage correctly')
        
    def test_get_usage(self):
        conn = sl.connect('app.db')
        
        cursor = conn.cursor()
        cursor.execute("DROP TABLE usage")
        cursor.execute("CREATE TABLE usage (decTime TEXT, usage INTEGER)")
        cursor.execute("INSERT INTO usage VALUES (0,2345432)")
        cursor.execute("INSERT INTO usage VALUES (0.25,2345432)")
        conn.commit()
        
        meter = SmartMeter()
        substation = Substation(2345432,[meter])
        self.assertEqual(substation.getUsage(), 2345432, 'Substation did not return the attribute usage')
        substation.getSmartMeterUsage()

if __name__ == "__main__":
    unittest.main()
