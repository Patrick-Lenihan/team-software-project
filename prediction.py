import sqlite3 as sl
connect = sl.connect('app.db')
cursor = connect.cursor()

class Prediction():
    def __init__(self):
        self.usage = 0
        self.time = 0
        self.day = 0
        self.history = [0,0,0,0,0]
    
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
                self.day = 4
        
    def getHistoricalData(self):
        time = self.time
        use_history = [] # last 5 values to compare with current use
        historical_prediction = [] # next 5 values predict with current use 
        
        with connect:
            for i in range(5):
                time = self.checkTimeValue(time)
                cursor.execute('SELECT AVG(use) FROM use_history WHERE time = %f'%(time))
                for value in cursor:
                    average = value
                use_history.append(float(average[0]))
                time += -.25
                
                
            time = self.time
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
        with connect:
            cursor.execute('UPDATE use_history SET use='+str(self.usage)+' WHERE time='+str(self.time)+' AND day='+str(self.day))
        
    def predict(self, usage):
        self.usage = usage
        self.history.pop(0)
        self.history.append(self.usage) # remove oldest values and replace with new data
        
        historical_data, historical_prediction = self.getHistoricalData()
        self.updateHistoricalData()

        max_difference = 0 # biggest difference between a predicted value and its historical average
        
        print(self.history)
        print(historical_prediction)
        for i in range(len(historical_data)):
            if historical_data[i] < self.history[i] and (self.history[i] - historical_data[i]) > max_difference:
                max_difference = self.history[i] - historical_data[i]
        
        for i in range(len(historical_prediction)):
            historical_prediction[i] += max_difference
        print(historical_data)
        self.time += .25 # increment time for the next request  
        
        self.time = self.checkTimeValue(self.time)
        self.checkDayValue()
        
        return historical_prediction
                
if __name__ == '__main__':
    prediction = Prediction()
    print(prediction.predict(5000))  
                