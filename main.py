"""
This is the main controller module of the power grid.

it effectively acts as the controller for the entire power grid staying in an infinite loop and
calling relevant modules when necessary.

Typical usage example:
controller = Main(distributionObject,listOfProducerObjects)
controller.Iterate()
"""
class Main():
    """
    This is the main class.

    it has one public method Iterate()
    """
    def __init__(self, distribution, producers):
        """
        the initialiser for the Main class

        Args:
            distribution: a distribution object
            producers: a list of producer objects
        """
        self.distribution = distribution
        self.producers = producers
        self.prediction = Prediction()
        self.market = Market()

    def Iterate(self):
        """
        the method that runs controller simulation

        the method that runs in an endless loop and calls other modules when needed,
        to send information or run processes on each object.
        """
        time = 0
        while True:
            usage = self.getUsage(time)
            totalProduction = self.pollProducers()

            predictions = self.getPredictions(usage)
            winners, price = self.maket.getWinners()

            self.sendOrders(winners)
            self.distribution.receivePrice(price)

            time += 1

    def getUsage(self, time):
        return self.distribution.usage(time)

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
            total_energy += i.currentProduction
        return total_energy

    def getPredictions(self, usage):
        return self.prediction.predict(usage)

    def sendOrders(self, winners):
        """
        sends the orders to the producers

        sends the orders that have been decided by the market module to each producer in the 
        producers list.

        Args:
        winners: a dict with each producer as a key a list of how much energy they should produce
                for a given time period in the future 
                eg.
                {
                	producer: [amount,amount.....],
                }
        """
        for i in self.producers:
            i.receiveOrder(winners[i])

