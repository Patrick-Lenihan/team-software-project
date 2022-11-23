import unittest
import sqlite3 as sl
from controller.prediction import Prediction

class TestPrediction(unittest.TestCase):
    def setup(self):
        '''
        Setup run at the beginning of each test to ensure clean database for each test.
        Can be called again where the database is changed and more tests are required.
        'use' values in the table are unique in this example for tracing bugs and 
        to avoid false positive tests.
        '''
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
            
            for i in range(5):# days
                for j in range(24): # hours
                    for k in range(4):
                        self.connect.execute('''INSERT INTO use_history (use, time, day) VALUES (%d*96+%d*4+%d, %f, %d)'''%(i,j,k,j+k*.25,i))
        self.prediction = Prediction()

    def test_check_time_value(self):
        self.setup()
        time = self.prediction.checkTimeValue(4.5)
        self.assertEqual(time, 4.5, 'valid time was reset incorrectly')
        
        time = self.prediction.checkTimeValue(-0.25)
        self.assertEqual(time, 23.75, 'time underflow was not handled')
        
        time = self.prediction.checkTimeValue(24)
        self.assertEqual(time, 0, 'time overflow was not handled')
        
    def test_check_day_value(self):
        self.setup()
        self.prediction._time = 0
        self.prediction.day = 0
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 1, 'day value was not incremented')
        
        self.prediction._time = 0
        self.prediction.day = 4
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 0, 'day value was not reset to 0')
        
        self.prediction._time = 23.75
        self.prediction.day = 1
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 0, 'day value was not decremented')
        
        self.prediction._time = 23.75
        self.prediction.day = 0
        self.prediction.checkDayValue()
        self.assertEqual(self.prediction.day, 4, 'day value did not underflow back to 4')
        
    def test_get_historical_predictions(self):
        self.setup()
        history, prediction = self.prediction.getHistoricalData()
        self.assertEqual(prediction, sorted(prediction), 'test db should return sorted history')
        self.assertEqual(history[-1], prediction[0], 'current usage should be contained in both lists')
        
        self.assertEqual(len(history), 5, 'returned history should contain 5 averages')
        self.assertEqual(len(prediction), 5, 'returned trend should contain 5 averages')
        
        # test that prediction hold average use at that time
        cursor = self.connect.cursor()
        cursor.execute('SELECT use FROM use_history WHERE time = 0')
        uniqueValues = []
        for value in cursor:
            uniqueValues.append(int(value[0]))
        self.assertEqual(
            sum(uniqueValues)/len(uniqueValues),
            prediction[0],
            'values in historical trend should be the averages at that time',
        )
        
    def test_update_historical_data(self):
        self.setup()
        self.prediction._time = 0
        self.prediction.day = 0
        self.prediction.predict(1234321)
        
        cursor = self.connect.cursor()
        cursor.execute('SELECT use FROM use_history WHERE time = 0 AND day = 0')
        for value in cursor:
            use = int(value[0])
        self.assertEqual(use, 1234321, 'database not updated with current usage')
        
    def test_predict(self):
        self.setup()
        previous_value = self.prediction.history[-1]
        self.prediction._time = 5
        historical_prediction = self.prediction.predict(44)
        self.assertNotEqual(previous_value, self.prediction.history[-1], 'history attribute not updated with current usage')
        self.assertEqual(self.prediction.history[-1], 44)
       
        self.setup()
        historical_prediction = self.prediction.predict(400)
        # adjusts to new higher use with same historical trend
        self.assertEqual(
            historical_prediction,
            [401.0, 402.0, 403.0, 404.0, 405.0],
            'prediction with high usage should increase with max difference',
        )


if __name__ == "__main__":
    unittest.main()
