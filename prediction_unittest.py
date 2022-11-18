import unittest
import sqlite3 as sl
from prediction import Prediction

class TestPrediction(unittest.TestCase):
    def setup(self):
        self.connect = sl.connect('app.db')
        with self.connect:
            self.connect.execute("""DROP TABLE IF EXISTS use_history;""")
            self.connect.execute("""
                        CREATE TABLE use_history
                        (
                            use FLOAT,
                            time FLOAT,
                            day INTEGER
                        );""")
            
            # each usage in database given unique values to avoid false positive tests
            for i in range(5):# days
                for j in range(24): # hours
                    for k in range(4):
                        self.connect.execute('''INSERT INTO use_history (use, time, day) VALUES (%d*96+%d*4+%d, %f, %d)'''%(i,j,k,j+k*.25,i))
        self.prediction = Prediction()

    def test_check_time_value(self):
        self.setup()
        time = self.prediction.checkTimeValue(4.5)
        self.assertEqual(time, 4.5)
        
        time = self.prediction.checkTimeValue(-0.25)
        self.assertEqual(time, 23.75)
        
        time = self.prediction.checkTimeValue(24)
        self.assertEqual(time, 0)
        
    def test_check_day_value(self):
        self.setup()
        self.prediction.time = 0
        self.prediction.day = 0
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 1)
        
        self.prediction.time = 0
        self.prediction.day = 4
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 0)
        
        self.prediction.time = 23.75
        self.prediction.day = 1
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 0)
        
        self.prediction.time = 23.75
        self.prediction.day = 0
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 4)
        
    def test_get_historical_predictions(self):
        self.setup()
        history, prediction = self.prediction.getHistoricalData()
        self.assertEqual(prediction, sorted(prediction))
        self.assertEqual(history[-1], prediction[0])
        
        self.assertEqual(len(history), 5)
        self.assertEqual(len(prediction), 5)
        
        # test that prediction hold average use at that time
        cursor = self.connect.cursor()
        cursor.execute('SELECT use FROM use_history WHERE time = 0')
        uniqueValues = []
        for value in cursor:
            uniqueValues.append(int(value[0]))
        self.assertEqual(sum(uniqueValues)/len(uniqueValues), prediction[0])
        
    def test_update_historical_data(self):
        self.setup()
        self.prediction.time = 0
        self.prediction.day = 0
        self.prediction.predict(1234321)
        
        cursor = self.connect.cursor()
        cursor.execute('SELECT use FROM use_history WHERE time = 0 AND day = 0')
        for value in cursor:
            use = int(value[0])
        self.assertEqual(use, 1234321)
        
    def test_predict(self):
        self.setup()
        previous_value = self.prediction.history[-1]
        self.prediction.time = 5
        historical_prediction = self.prediction.predict(44)
        self.assertNotEqual(previous_value, self.prediction.history[-1])
        self.assertEqual(self.prediction.history[-1], 44)
        # inputted list has average usage at the next times, showing when use is below historic average, prediction is kept at historic average
        self.assertEqual(historical_prediction, [212.0, 213.0, 214.0, 215.0, 216.0])
        
        self.setup()
        historical_prediction = self.prediction.predict(400)
        # adjusts to new higher use with same historical trend
        self.assertEqual(historical_prediction, [400.0, 401.0, 402.0, 403.0, 404.0])


if __name__ == "__main__":
    unittest.main()
