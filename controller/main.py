import controller.prediction as prediction
import controller.market as market
import time
"""
This is the main controller module of the power grid.

it effectively acts as the controller for the entire power grid staying in an infinite loop and
calling relevant modules when necessary.

Typical usage example:
controller = Main(substationObject,listOfProducerObjects)
controller.Iterate()
"""
class Main():
    """
    This is the main class.

    it has one public method Iterate()
    """
    def __init__(self, main_substation, producers,substations,smartMeters):
        """
        the initialiser for the Main class

        Args:
            main_substation: a substation object
            producers: a list of producer objects
        """
        self.main_substation = main_substation
        self.producers = producers
        self.prediction = prediction.Prediction()
        self.market = market.Market(producers)
        self.substations = substations
        self.smartMeters = smartMeters
        self.seq_num = 0

    def Iterate(self):
        """
        the method that runs controller simulation

        the method that runs in an endless loop and calls other modules when needed,
        to send information or run processes on each object.
        """
        time = 0
        fails = 0 
        result_info = dict()
        while True:
            try:
                usage = self.getUsage()
                self.seq_num += 1
                totalProduction = self.pollProducers()
                
                totalProduction, usage, battery_discharge, battery_level = self.manageBatteries(totalProduction, usage)
                
            
                self.checkFaultDetection()
                
                print("<------------------------------------>")
                
                if totalProduction < usage:
                    fails +=1
                    print('FAIL -', usage - totalProduction)
                print("Time:", time/4)
                print("Usage:",usage)
                if battery_discharge != 0:
                    print('Battery Discharge:',battery_discharge)
                print("Total Production:",totalProduction)
                print("Battery Level", battery_level)
                print()
            
                predictions = self.getPredictions(usage)
                winners = self.market.GetWinners(predictions)

                self.sendOrders(winners)

                result_info[time/4] = {"usage":usage,"totalProduction":totalProduction,"battery_discharge":battery_discharge,"battery_level":battery_level,"winners":winners}

                time += 1
            except:
                print("No more usage data")
                print("num fails:",fails)
                return result_info, fails, self.checkFaultDetection()


    def getUsage(self):
        return self.main_substation.getUsage()

    def pollProducers(self):
        """
       retrieves the current power production.

        an internal method that loops through the producers and asks them how much they are
        generating and

        Returns:
            the total energy produced at a given time

        """
        total_energy = 0
        for i in self.producers:
            total_energy += i.current_production
        return total_energy

    def getPredictions(self, usage):
        return self.prediction.predict(usage)

    def sendOrders(self, winners):
        """
        sends the orders to the producers

        sends the orders that have been decided by the market module to each producer in the 
        producers list.

        Args:
        winners: a dict with each producer as a key a list of bid objects containing 
        		how much energy they should producefor a given time period in the future 
                eg.
                {<producer_object>: [<bid_object>,<bid_object>.....]} 
        """
        for i in self.producers:
            i.receiveOrder(winners[i])

    def manageBatteries(self, totalProduction, usage):
        battery_discharge = 0
        battery_level = 0
        if totalProduction > usage:
            energy_to_store = totalProduction - usage
            for substation in self.substations:
                energy_to_store = substation.store_battery(energy_to_store)
                battery_level += substation._battery.getCurrentlyStored()
        else:
            battery_discharge = totalProduction
            for substation in self.substations:
                if totalProduction < usage:
                    totalProduction += substation.discharge_battery((usage-totalProduction))
                battery_level += substation._battery.getCurrentlyStored()
            battery_discharge = totalProduction - battery_discharge
            
        return totalProduction, usage, battery_discharge, battery_level
    
    def checkFaultDetection(self):
        for substation in self.substations:
            if not substation.hasConnection(self.seq_num):
                print("fault detected!")
                return True
        return False