import unittest
import sqlite3 as sl
from substation import Substation
from smartmeter import SmartMeter
class TestSubstation(unittest.TestCase):

    '''
    Test the smart meter usage
    '''

    def testGetSmartMeterUsage(self):
        meter1 = SmartMeter()
        usage = 1234321
        substation = Substation(usage,[])
        self.assertEqual(substation.getUsage(), usage, 'Substation did not return the attribute usage')
        
        # another test with meters)):

    def test_get_smart_meter_usage(self):
        meter1 = SmartMeter(0000000000000)
        #... more meters
        substation = Substation(0,[])
        substation.getSmartMeterUsage()
        self.assertEqual(substation._usage, 'value', 'substation did not calculate total usage correctly')
        
    def test_get_usage(self):
        usage = 1234321
        substation = Substation(usage,[])
        self.assertEqual(substation.getUsage(), usage, 'Substation did not return the attribute usage')
        
        # another test with meters

if __name__ == "__main__":
    unittest.main()
