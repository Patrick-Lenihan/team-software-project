'''
The smart meter module is used to represent the end users of the system. 
For simulation purposes, the smart meter will receive data from the controller about the 
amount of electricity it has consumed. 

The smart meter will then receive the appropriate amount of electricity from the sub-station, 
as well as the current price and producer of the elecectricity supplied.

The smart meter class will be called several times by the controller, to represent several end users.
'''

class Meter(object):

    '''
    The meter class will be used to receive the current electricity consumption from the controller,
    as well as the current electricity price and producer.
    '''

    def __init__(self, usage, price, producer, output):

        '''
        The initialiser for the meter class

        Args:
            usage: the amount of electricity used at a given time (sent from the main controller)
            received: the amount of electricity received at a given time (sent from the substation)
            price: the current price of electricity (sent from the controller)
            producer: the current producer of electricity (sent from the controller)
        '''

        self._usage = usage
        self._received = price
        self._price = producer
        self._producer = output
        

    def getUsage(self, usage):

        '''
        Gets the current electricity usage from the controller 

        Args:
            usage: the amount of electricity used at a given time
        '''

        self.usage = self.main.getUsage()

    def getElectricity(self):

        '''
        Gets the current electricity produced, as well as the price and producer from the substation.

        Args:
            received: the amount of electricity received at a given time
            price: the current price of electricity
            producer: the current producer of electricity
        '''

        self.received = self.substation.getElectricity()
        self.price = self.substation.getPrice()
        self.producer = self.substation.getProducer()

    def sendRequest(self):

        '''
        Sends a request to the controller if more or less electricity is required.
        '''

        if self.usage < self.received:
            self.main.powerstation.rampUp(self.received - self.usage) # Should talk to controller first, but these methods are not yet implemented
        elif self.usage > self.received:
            self.main.powerstation.rampDown(self.usage - self.received) 

    
    