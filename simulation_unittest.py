import unittest
import simulation
import gridClasses.smartmeter as smartmeter
import gridClasses.substation as substation
import gridClasses.powerstation as powerstation

class TestNormal(unittest.TestCase):
    def test_NoFails(self):
        sim = simulation.Simulation()
        _, fails, _= sim.getResults()
        self.assertEqual(0,fails,"whoops a nationwide blackout occored")
    def test_for_no_fault(self):
        sim = simulation.Simulation()
        _,_,has_fault= sim.getResults()
        self.assertEqual(False,has_fault,"a breakage has been detected without atualy being there")

class SimWithFault(simulation.Simulation):
    def __init__(self):
        super().__init__()
    def generateDistribution(self):
        smartmeters = [smartmeter.SmartMeter(), smartmeter.SmartMeter(),smartmeter.SmartMeter(),smartmeter.SmartMeter()]
        second_substation = substation.Substation(0, smartmeters[0:2],[])
        main_substation = substation.Substation(0, smartmeters[2:],[second_substation])
        substations = [main_substation,second_substation,substation.Substation(0,[],[])]

        return smartmeters,substations

class TestFault(unittest.TestCase):
    def test_for_fault(self):
        sim = SimWithFault()
        _,_,has_fault= sim.getResults()
        self.assertEqual(True,has_fault,"a breakage has occored in the line without being detected")
    def test_NoFails(self):
        sim = simulation.Simulation()
        _, fails, _= sim.getResults()
        self.assertEqual(0,fails,"whoops a nationwide blackout occored")

class SimWithUneededFosilFuels(simulation.Simulation):
    def __init__(self):
        super().__init__()
    def generateProducers(self):
        producers = []
        producers.append(powerstation.Producer(3.35, 0, 2000))
        producers.append(powerstation.Producer(2.35, 1, 4000))
        producers.append(powerstation.Producer(3.31, 0, 3000))
        producers.append(powerstation.Producer(2.32, 3, 4000))
        producers.append(powerstation.Producer(3.34, 0, 5000))
        producers.append(powerstation.Producer(2.35, 1, 4000))
        producers.append(powerstation.FossilFuelPlant(2.00,4,2000,500))

        return producers


class TestEnvironmentalyFriendlieness(unittest.TestCase):
    def test_does_not_fossil_fuels(self):
        fossil_fuel_bid = False
        sim = SimWithUneededFosilFuels()
        results,_,has_fault = sim.getResults()
        for i in results:
            for val_list in results[i]["winners"].values():
                for val in val_list:
                    if isinstance(val,int):
                        continue
                    if isinstance(val.producer,powerstation.FossilFuelPlant):
                        if val.amount_electrictiy != 0:
                            fossil_fuel_bid = True
                        
        self.assertEqual(False,fossil_fuel_bid,"a FossilFuelPlant was used unnecessarily")
    def test_NoFails(self):
        sim = SimWithUneededFosilFuels()
        _, fails, _= sim.getResults()
        self.assertEqual(0,fails,"whoops a nationwide blackout occored")
    def test_for_no_fault(self):
        sim = SimWithUneededFosilFuels()
        _,_,has_fault= sim.getResults()
        self.assertEqual(False,has_fault,"a breakage has been detected without atualy being there")


if __name__ == "__main__":
    unittest.main()

            

