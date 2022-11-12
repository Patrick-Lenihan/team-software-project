from random import randint
from bid import Bid

class Producer:
    def __init__(self,price,emmision_level,max_output):# inputs will be given, these are placeholders
        self.output = 0 
        self.price = price
        self.max_output = max_output
        self.emmision_level = emmision_level
        '''self.output = 0
        self.price = 43.27 # average cents KW/h
        self.emmision_level = 0 # used to know which queue it should be in for market
        self.max_output = 1000000000000000 # to be decided'''
        
    def getOutput(self):
        return self.output
    def getFutureBid(self,predictions):
        bids = []
        for i in predictions:
            bid = Bid(self.price,self,self.max_output,self.emmision_level)
            bids.append(bid)
        return bids

    
    current_production = property(getOutput)

        
class FossilFuelPlant(Producer):
    def __init__(self):
        super().__init__()
        self.rampUpLimit = 100
        
    def startRampUp(self, increase):
        # assume a fossil fuel plant can ramp 100MW every 15 mins till max output
        if increase > self.rampUpLimit:
            increase = self.rampUpLimit
        if increase + self.output > self.max_output:
            self.output = self.max_output
        else:
            self.output += increase

    def rampDown(self, decrease):
        if self.output - decrease < 0:
            self.output = 0
        else:
            self.output -= decrease
            

    def changeOutput(self, request):
        if request['timeTillRamp'] == 0 and request['amount']-self.output > 0:
            self.startRampUp(request['amount']-self.output) # Assumes request is total amount needed from producer
        elif request['amount']-self.output < 0:
            self.rampDown(abs(request['amount']-self.output))
            
    
            
class WindFarm(Producer):
    def __init__(self):
        super().__init__()
        
    def calculateNextOutput(self):
        self.output += randint(-20,20)
        if self.output < 0:
            self.output = 0
        elif self.output > self.max_output:
            self.output = self.max_output


class HydroDam(Producer):
    def __init__(self):
        super().__init__()
        self.water_level = 95 # percentage of dam filled, assume 90% is max safe height, at least 40% needed
        self.output = 0
    
    def manageWaterLevel(self, request):
        self.checkWaterLevel()
        if self.water_level >= 90 and request:
            self.releaseWater()
    
    def checkWaterLevel(self):
        self.water_level += randint(0,2) # random for the possibility of rain
        
    def releaseWater(self):
        self.water_level -= 2 # this can be changed to 

    