'''the powerstation module contains the classes representing the energy production facilitys.

this file contains one producer superclass and some example subclasses of different types of
poducers.

'''
from random import randint
from controller.bid import Bid
import queue

class Producer(object):
    '''Producer is a generic energy producer class.
    Atributes:
        price: the price per unit of electricity.
        emmision_level: the emmision rating 1 being
                        good of the producer.
        max_output: the maximum amount of energy the
                    producer can produce at once.
    '''
    def __init__(self,price,emmision_level,max_output):
        '''the initaliser for the Producer class.
        sets self.output to 0
        '''
        self.output = 0 
        self.price = price
        self.max_output = max_output
        self.emmision_level = emmision_level
        
    def getOutput(self):
        return self.output
    def setOutput(self,new_output):
        self.output = new_output
    def getFutureBid(self,predictions):
        ''' getFutureBid calculates how much the 
        producer is willing to pay and producer given
        future predictions.
        it always bids the max output and will be overiden in
        most subclasses
        Args: 
            predictions: a list of the predicted electricity demand
                        in 15 min chunks.
            returns: a list of bid objects with the index zero being the bid
            for 15 mins time and index one is 30mins.....
        '''
        bids = []
        for i in predictions:
            bid = Bid(self.price,self,self.max_output,self.emmision_level)
            bids.append(bid)
        return bids

    def receiveOrder(self,orders):
        '''this function simulates the producer recieving the orders and predicted
        orders and acting accordingly.
        Args: 
            orders: a list of bid objects containing the orders and predicted orders
                    with index 0 being the order and the rest being predicted orders
                    in 15 min increments.
        '''
        self.output = orders[0].amount_electrictiy
        if self.max_output < self.output:
            self.output = self.max_output
    def __hash__(self):
        return hash((self.output,self.price,self.max_output,self.emmision_level))
    
    current_production = property(getOutput,setOutput)

        
class FossilFuelPlant(Producer):
    '''FossilFuelPlant is a type of producer that uses fossil fuels.
    its main difference is that it has a ramp up time before it can
    reach full capability from baseline.
    Atributes:
        price: the price per unit of electricity.
        emmision_level: the emmision rating 1 being
                        good of the producer.
        max_output: the maximum amount of energy the
                    producer can produce at once.
        rampUpLimit: the maximum amount that the plant can ramp up
                    every 15 mins.
    '''
    def __init__(self,price,emmision_level,max_output,rampUpLimit):
        super().__init__(price,emmision_level,max_output)
        self.rampUpLimit = rampUpLimit
        
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

    def getFutureBid(self,predictions):
        ''' getFutureBid calculates how much the 
        producer is willing to pay and producer given
        future predictions.
        it overides the original method in its superclass to take into
        account the 15min ramp up limit. this code takes into acount.
        this fact and bids accordingly
        Args: 
            predictions: a list of the predicted electricity demand
                        in 15 min chunks.
        Returns: a list of bid objects with the index zero being the bid
            for 15 mins time and index one is 30mins.....
        '''
        bids = []
        current_possable_output = self.output
        for i in predictions:
            if (current_possable_output + self.rampUpLimit)<= self.max_output:
                current_possable_output += self.rampUpLimit
            else:
                current_possable_output = self.max_output
            bid = Bid(self.price,self,current_possable_output,self.emmision_level)
            bids.append(bid)
        return bids
    def receiveOrder(self,orders):
        '''this function simulates the producer recieving the orders and predicted
        orders and acting accordingly.
        it overides the method in its superclass in order to take into acount the 
        ramp up limit. if it recieves an order for the future that is only possable to reach
        if it ramps up now it will ramp up immediatly in order to prevent its bid from being
        false.
        Args: 
            orders: a list of bid objects containing the orders and predicted orders
                    with index 0 being the order and the rest being predicted orders
                    in 15 min increments.
        '''
        if not orders:
            return
        orders = self.getElectricityFromOrders(orders)
        jumps, illigal_jumps = self.generateListOfJumps(orders)
        
        while not illigal_jumps.empty():
            bad_jump = illigal_jumps.get()
            jumps = self.reformatJumpsToLegal(jumps,bad_jump)

        if 0 < jumps[0]:
            self.startRampUp(jumps[0])
        else:self.rampDown(jumps[0]*-1)
    def getElectricityFromOrders(self,orders):
        for i in range(len(orders)):
            orders[i] = orders[i].amount_electrictiy
        return orders
    def generateListOfJumps(self,orders):
        '''loops through a list of bid orders
        and gets how much they increase by between
        each 15min increments(jumps).
        generates a queue of illigal jumps that are not
        possable given the ramp up limit.
        Args:
            orders: a list of units of electricity ordered
        '''
        jumps = [orders[0] - self.output]
        illigal_jumps = queue.Queue()
        i = 1
        while i < len(orders):
            jump = orders[i]- orders[i-1]
            jumps.append(jump)
            if self.rampUpLimit < jump:
                illigal_jumps.put({"Position":i,"jump: ":jump}) 
            i+=1
        return jumps, illigal_jumps
    def reformatJumpsToLegal(self,jumps,bad_jump):
        '''reformatJumpsToLegal takes in a jump that is not possable 
        given the ramp up limit and makes that jump possable by increasing
        previos jumps recursively.

        Args:
            jumps: a list of differences between list values
            bad_jump: the jump that is too high and must
                    be reduced by increasing the previos
                    jumps.
            
        '''
        index_to_change = bad_jump["Position"]
        i = index_to_change-1
        while True:
            if i < 0:
                return jumps
            if jumps[i] <= self.rampUpLimit:
                if jumps[index_to_change] - self.rampUpLimit < self.rampUpLimit- jumps[i]:
                    jumps[i] += jumps[index_to_change]-self.rampUpLimit
                    jumps[index_to_change] = self.rampUpLimit
                    return jumps
                else:
                    amount_to_change = self.rampUpLimit -  jumps[i]
                    jumps[i] += amount_to_change
                    jumps[index_to_change] -= amount_to_change
            i -= 1

            
class WindFarm(Producer):
    '''WindFarm is a producer that generates a variable amount of electricity and
    stores it in a battery object.
    Atributes:
        price: the price per unit of electricity.
        emmision_level: the emmision rating 1 being
                        good of the producer.
        max_output: the maximum amount of energy the
                    producer can produce at once.
        battery: a Battery object storing the power 
                generated by the windfarm
    '''
    def __init__(self,price,emmision_level,max_output,battery):
        super().__init__(price,emmision_level,max_output)
        self.battery = battery
        
    def calculateNextOutput(self):
        self.battery.store(randint(0,40))
    def getFutureBid(self,predictions):
        '''getFutureBid calculates how much the 
        producer is willing to pay and producer given
        future predictions.

        it overdes this meathod in its supperclass because it should not
        bid its maximum amount each time because then it would lead to
        erratic behavior from the system. it should instead bid evenly across
        all predicted times the maximum amount that is possable without 
        draining reserves.

        Args: 
            predictions: a list of the predicted electricity demand
                        in 15 min chunks.
        Returns: a list of bid objects with the index zero being the bid
            for 15 mins time and index one is 30mins.....

        '''
        amount_stored = self.battery.currently_stored
        bids = []
        amount_to_bid = amount_stored//len(predictions)
        for prediction in predictions:
            bids.append(Bid(self.price,self,amount_to_bid,self.emmision_level))
        return bids
    def receiveOrder(self,orders):
        self.battery.discharge(orders[0].amount_electrictiy)
        self.output = orders[0].amount_electrictiy
        self.calculateNextOutput()
            

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


class Battery(object):
    '''an object used to represent a battery storage facility

    Atributes:
        max_stored: the max amount of electricity that this
                    facility can store.
        currently_stored: the amount of electricty currenly stored
                            in the facility.
    '''
    def __init__(self,max_stored,currently_stored):
        self.max_stored = max_stored
        self.currently_stored = currently_stored
    def discharge(self, amount_needed):
        self.currently_stored -= amount_needed
        if self.currently_stored < 0:
            self.currently_stored = 0
    def store(self,amount):
        self.currently_stored += amount
        if self.currently_stored > self.max_stored:
            self.currently_stored = self.max_stored