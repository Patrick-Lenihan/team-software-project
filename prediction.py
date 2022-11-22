import sqlite3 as sl
connect = sl.connect('app.db')
cursor = connect.cursor()


class Prediction():
    '''
    Module generates a prediction of the usage needed in the next hour..
    '''
    def __init__(self):
        
        '''
        The initialiser for the Prediction class

        Args:
            time: current time being stored as a float and increments in 15 minute jumps
            day: value from 0-4 used to track only the last 5 days usage
            history: last 5 recorded total usages for the grid
        '''
        self._time = 0
        self.day = 0
        self.history = [0,0,0,0,0]
    
    def checkTimeValue(self, time):
        '''
        Check if time value has overflowed or underflowed
        Can be reset with the start of a new day

        Args:
            time: current time after being incremented
            
        Returns:
            time: current time after checking for underflows and overflows
        '''
        if time == 24:
            time = 0
        if time < 0:
            time = 23.75
        return time
    
    def checkDayValue(self):
        '''
        Check if day value needs to be incremented or decremented depending on time value
        Can be reset with the start of a new day

        Args:
            time: current time after being incremented
            
        '''
        if self._time == 0:
            self.day += 1
            if self.day == 5:
                self.day = 0
        elif self._time == 23.75:
            self.day -= 1
            if self.day == -1:
                self.day = 4
        
    def getHistoricalData(self):
        '''
        Gets historical data for the current time pver the past 5 days

        Returns:
            use_history: average of the past 5 usages from the current time including current usage
            historical_prediction: average of the next 5 usages at the current time including current usage
        '''
        time = self._time
        use_history = [] # last 5 values to compare with current use
        historical_prediction = [] # next 5 values predict
        
        with connect:
            for i in range(5):
                time = self.checkTimeValue(time)
                cursor.execute('SELECT AVG(use) FROM use_history WHERE time = %f'%(time))
                for value in cursor:
                    average = value
                use_history.append(float(average[0]))
                time += -.25
                
                
            time = self._time + .25
            for i in range(5):
                time = self.checkTimeValue(time)
                cursor.execute('SELECT AVG(use) FROM use_history WHERE time = %f'%(time))
                for value in cursor:
                    average = value
                historical_prediction.append(float(average[0]))
                time += .25
                
        use_history.reverse()
        return use_history, historical_prediction
        
    def updateHistoricalData(self):
        '''
        Updates Historical trend database with current usage
        '''
        with connect:
            cursor.execute('UPDATE use_history SET use='+str(self.history[-1])+' WHERE time='+str(self._time)+' AND day='+str(self.day))
        
    def predict(self, usage):
        '''
        Takes in recent usage and compares it to historical trend. 
        In the event that recent usage is below historical usage for a given time, historical trend is used.
        Where recent usage is greater than historical trend, 
        the historical trend line is pushed up to intersect the recent usage and this altered trend is used.

        Args:
            time: current time after being incremented
            
        '''
        self.history.pop(0)
        self.history.append(usage) # remove oldest values and replace with new data
        
        historical_data, historical_prediction = self.getHistoricalData()
        self.updateHistoricalData()

        max_difference = 0 # biggest difference between a predicted value and its historical average
        
        for i in range(len(historical_data)):
            if historical_data[i] < self.history[i] and (self.history[i] - historical_data[i]) > max_difference:
                max_difference = self.history[i] - historical_data[i]
        
        for i in range(len(historical_prediction)):
            historical_prediction[i] += max_difference
        self._time += .25 # increment time for the next request  
        
        self._time = self.checkTimeValue(self._time)
        self.checkDayValue()
        
        return historical_prediction
                
if __name__ == '__main__':
    prediction = Prediction()
    print(prediction.predict(5000))  
                