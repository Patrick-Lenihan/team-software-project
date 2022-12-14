'''
The substation acts as a distributer of electricity for end users.
It takes usage from the connected households to calculate
the total power being consumed.
This data is sent on to the controller to help regulate production.
'''
from gridClasses.powerstation import Battery

class Substation(object):

    '''
    The Substation receives data from Smart Meters and passes it on to the controller.
    '''

    def __init__(self, usage, users,substations):
    
        '''
        The initialiser for the meter class

        Args:
            usage: the amount of electricity used at a given time by all connected Smart Meters
            users: list of all connected Smart Meters
        '''

        self._usage = usage
        self._users = users
        self._battery = SubstationBattery(150, 150)
        self._substations = substations
        self.seq_num = 0

    def getSmartMeterUsage(self):

        '''
        Calculates the current electricity usage from all connected homes
        '''
        self._usage = 0
        for user in self._users:
            self._usage += user.updateUsage()
        for substation in self._substations:
            self._usage += substation.getUsage()

    def getUsage(self):

        '''
        Gives back the total electricity usage of all connected homes to the controller

        Returns:
            usage: the amount of electricity being supplied through substation to homes
        '''
        self.getSmartMeterUsage()
        self.seq_num +=1
        return self._usage
    
    def discharge_battery(self, amount):
        return self._battery.discharge(amount)
        
    def store_battery(self, amount):
        return self._battery.store(amount)

    def hasConnection(self,seq_num):
        if self.seq_num == seq_num:
            return True
        return False
        
        
class SubstationBattery(Battery):
    '''an object used to represent a battery storage facility in a substation

    Atributes:
        max_stored: the max amount of electricity that this
                    facility can store.
        currently_stored: the amount of electricty currenly stored
                            in the facility.
                            
    returns: excess electricity unable to store
    '''
    def store(self,amount):
        starting_level = self.currently_stored
        
        self.currently_stored += amount
        if self.currently_stored > self.max_stored:
            self.currently_stored = self.max_stored
        return amount - (self.currently_stored - starting_level)

    def discharge(self, amount_needed):
        difference = 0
        self.currently_stored -= amount_needed
        if self.currently_stored < 0:
            difference = self.currently_stored
            self.currently_stored = 0
        return amount_needed + difference
    
    def getCurrentlyStored(self):
        return self.currently_stored