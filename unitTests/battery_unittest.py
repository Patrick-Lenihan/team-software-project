import unittest
from gridClasses.substation import SubstationBattery

class TestSubstationBattery(unittest.TestCase):

    def test_get_current_level(self):
        battery = SubstationBattery(150, 100)
        self.assertEqual(battery.getCurrentlyStored(), 100, 'Substation Battery did not return correct level')
        
    def test_discharge(self):
        battery = SubstationBattery(150, 100)
        self.assertEqual(battery.discharge(20), 20, 'Substation Battery did not discharge the correct amount')
        
        self.assertEqual(battery.discharge(100), 80, 'Substation Battery did not discharge remaining electricity')

        self.assertEqual(battery.discharge(20), 0, 'Substation Battery level was incorrect')
        
    def test_store(self):
        battery = SubstationBattery(150, 100)
        self.assertEqual(battery.store(20), 0, 'Substation Battery did not store the correct amount')
        
        self.assertEqual(battery.store(100), 70, 'Substation Battery did not return remaining electricity')
        
    

if __name__ == "__main__":
    unittest.main()
