import prediction
import market
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
    def __init__(self, substation, producers):
        """
        the initialiser for the Main class

        Args:
            substation: a substation object
            producers: a list of producer objects
        """
        self.substation = substation
        self.producers = producers
        self.prediction = prediction.Prediction()
        self.market = market.Market(producers)

    def Iterate(self):
        """
        the method that runs controller simulation

        the method that runs in an endless loop and calls other modules when needed,
        to send information or run processes on each object.
        """
        time = 0
        
        while True:

            try:
                usage = self.getUsage()
                totalProduction = self.pollProducers()

                print("<------------------------------------>")

                if totalProduction <= usage:
                    print('FAIL -', usage - totalProduction)
                print("Time:", time/4)
                print("Usage:",usage)
                print("Total Production:",totalProduction)
                print()
            
                predictions = self.getPredictions(usage)
                winners = self.market.GetWinners(predictions)

                self.sendOrders(winners)

                time += 1

            except:
                print("No more usage data")
                break

    def getUsage(self):
        return self.substation.getUsage()

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

