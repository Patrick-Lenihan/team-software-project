'''
The substation acts as a distributer of electricity for end users.
It takes usage from the connected households to calculate
the total power being consumed.
This data is sent on to the controller to help regulate production.
'''

class Substation(object):

    '''
    The Substation receives data from Smart Meters and passes it on to the controller.
    '''

    def __init__(self, usage, users):

        '''
        The initialiser for the meter class

        Args:
            usage: the amount of electricity used at a given time by all connected Smart Meters
            users: list of all connected Smart Meters
        '''

        self._usage = usage
        self._users = users
        

    def getSmartMeterUsage(self):

        '''
        Calculates the current electricity usage from all connected homes
        '''
        self._usage = 0
        for user in self.users:
            self._usage += user.getUsage()

    def getUsage(self):

        '''
        Gives back the total electricity usage of all connected homes to the controller

        Returns:
            usage: the amount of electricity being supplied through substation to homes
        '''
        self.getSmartMeterUsage()
        return self._usage
    
    