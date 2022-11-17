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
        print(history, prediction)
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
        
"""
        def test_dequeue(self):
            test_queue = PQ()
            test_bids_to_add = [[Bid(300, 0, 200, 2),
                                 Bid(100, 0, 200, 2),
                                 Bid(200, 0, 200, 2),
                                 Bid(250, 0, 200, 2)],
                                [Bid(315, 0, 200, 2),
                                 Bid(200, 0, 200, 2)]]
            wanted_results = [[300],
                              []]
            message = "PQ.dequeue"
            for test in range(len(test_bids_to_add)):
                test_queue.q = []
                for item in test_bids_to_add[test]:
                    test_queue.add(item)
                for i in range(3):
                    test_queue.dequeue()
                self.assertEqual(get_amounts_bid(test_queue.q),
                                 wanted_results[test], message)


class TestMultiLevelQueue(unittest.TestCase):
    def test_add(self):
        test_MLQ = MultiLevelQueue()
        test_bids_to_add = [Bid(300, 0, 200, 1),
                            Bid(100, 0, 200, 2),
                            Bid(200, 0, 200, 3),
                            Bid(250, 0, 200, 5)]
        wanted_result = [[], [300], [100], [200], [], [250]]
        for i in range(len(test_bids_to_add)):
            test_MLQ.add(test_bids_to_add[i])
        for i in range(len(test_MLQ._top_level_list)):
            #print("test_MLQ",get_amounts_bid(test_MLQ._top_level_list[i].q),"wr: ",wanted_result[i])
            self.assertEqual(get_amounts_bid(
                test_MLQ._top_level_list[i].q), wanted_result[i])


class TestMarket(unittest.TestCase):
    def test_GetWinners(self):
        producers = [Producer(1.3, 1, 200),
                     Producer(1.6, 1, 300),
                     Producer(2.4, 2, 300),
                     Producer(1.4, 3, 1000)]
        test_market = Market(producers)
        predictions = [500, 300, 1000]
        winners = test_market.GetWinners(predictions)
        wanted_results = {producers[0]: [Bid(1.3, producers[0], 200, 1), Bid(1.3, producers[0], 200, 1), Bid(1.3, producers[0], 200, 1)],
                          producers[1]: [Bid(1.6, producers[1], 300, 1), Bid(1.6, producers[1], 100, 1), Bid(1.6, producers[1], 300, 1)],
                          producers[2]: ["Nothing", "Nothing", Bid(2.4, producers[2], 300, 2)],
                          producers[3]: ["Nothing", "Nothing", Bid(1.4, producers[3], 200, 3)],
                          }
        # print(winners,"blip",wanted_results)
        for i in producers:
            # if i in winners:
            # print("winner:",get_amounts_bid(winners[i]))
            # if i  in wanted_results:
            # print("got",get_amounts_bid(winners[i]))
            # print("want",get_amounts_bid(wanted_results[i]))
            self.assertEqual(get_amounts_bid(
                winners[i]), get_amounts_bid(wanted_results[i]), "oops")
"""

if __name__ == "__main__":
    unittest.main()
