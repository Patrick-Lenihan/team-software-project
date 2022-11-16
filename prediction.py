import sqlite3 as sl
from queue import Queue
connect = sl.connect('app.db')
cursor = connect.cursor()

class Prediction():
    def __init__(self):
        self.usage = 50 # last usage
        self.time = 0
        self.day = 0
        self.history = Queue(maxsize=5)
        self.history.put(0) # fill last 5 recorded usages with default values
        self.history.put(0)
        self.history.put(0)
        self.history.put(0)
        self.history.put(0)
    
    def checkTimeValue(self, time):
        if time == 24:
            time = 0
        if time < 0:
            time = 23.75
        return time
    
    def checkDayValue(self):
        if self.time == 0:
            self.day += 1
            if self.day == 5:
                self.day = 0
        elif self.time == 23.75:
            self.day -= 1
            if self.day == -1:
                self.day = 5
        
    def getHistoricalData(self):
        time = self.time
        use_history = [] # last 5 values to compare with current use
        historical_prediction = [] # next 5 values predict with current use 
        
        with connect:
            for i in range(5):
                cursor.execute('SELECT AVG(use) FROM use_history WHERE time = %f'%(time))
                for value in cursor:
                    average = value
                use_history.append(float(average[0]))
                time += -.25
                self.checkTimeValue(time)
                
            time = self.time
            for i in range(5):
                cursor.execute('SELECT AVG(use) FROM use_history WHERE time = %f'%(time))
                for value in cursor:
                    average = value
                historical_prediction.append(float(average[0]))
                time += .25
                self.checkTimeValue(time)
        
        return use_history.reverse(), historical_prediction
        
    def updateHistoricalData(self):
        with connect:
            cursor.execute('UPDATE use_history SET use='+str(self.usage)+', time='+str(self.time)+', day='+str(self.day)+' WHERE time='+str(self.time)+' AND '+str(self.day))
        
    def predict(self, usage):
        self.history.get()
        self.history.put(self.usage) # remove oldest values and replace with new data
        self.updateHistoricalData()
        historical_data, historical_prediction = self.getHistoricalData()
        
        max_difference = 0 # biggest difference between a predicted value and its historical average
        self.usage = usage
        for i in range(len(historical_data)):
            if historical_data[i] < self.history[i] and (self.history - historical_data[i]) > maxDifference:
                maxDifference = self.history - historical_data[i]
        for i in range(len(historical_prediction)):
            historical_prediction[i] += max_difference
        self.time += .25 # increment time for the next request  
        
        self.time = self.checkTimeValue(self, self.time)
        self.checkDayValue(self)
        
        return historical_prediction
                
if __name__ == '__main__':
    prediction = Prediction()
    print(prediction.predict(6220))  
                