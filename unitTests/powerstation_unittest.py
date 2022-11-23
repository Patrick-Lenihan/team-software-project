from gridClasses.powerstation import *
import unittest

class TestProducer(unittest.TestCase):
	def test_getFutureBid(self):
		testProducer = Producer(12,1,33)
		predictions = [3,3,3,3]
		got = testProducer.getFutureBid(predictions)

		for i in range(len(predictions)):
			self.assertEqual(got[i].amountBid,12,"did not bid the expected amount for input")

class TestFossilFuelPlant(unittest.TestCase):
	def test_getFutureBid(self):
		tests= [{
		"Producer": FossilFuelPlant(12,1,50,10),
		"wanted bids": [10,20,30,40,50]
		},{
		"Producer": FossilFuelPlant(12,1,50,15),
		"wanted bids": [15,30,45,50,50]
		}]
		predictions = [100,100,100,100,100]
		
		for test in tests:
			got = test["Producer"].getFutureBid(predictions)
			got = formatBidList(got)
			self.assertEqual(got,test["wanted bids"],"your future bid did not match the expected")
	def test_receiveOrder(self):
		tests = [{
		"orders":[
				Bid(0,0,10,0),
				Bid(0,0,20,0),
				Bid(0,0,30,0),
			],
		"max_output":50,
		"ramp_up_limit":10,
		"wanted_output": 10,
		"output": 0
		},{
		"orders":[
				Bid(0,0,10,0),
				Bid(0,0,20,0),
				Bid(0,0,60,0),
			],
		"max_output":70,
		"ramp_up_limit":20,
		"wanted_output": 20,
		"output": 0
		},{"orders":[
				Bid(0,0,10,0),
				Bid(0,0,20,0),
				Bid(0,0,55,0),
			],
		"max_output":70,
		"ramp_up_limit":20,
		"wanted_output": 15,
		"output": 0
		},{"orders":[
				Bid(0,0,20,0),
				Bid(0,0,20,0),
				Bid(0,0,60,0),
			],
		"max_output":20,
		"ramp_up_limit":20,
		"wanted_output": 20,
		"output": 0
		},{"orders":[
				Bid(0,0,10,0),
				Bid(0,0,20,0),
				Bid(0,0,10,0),
				Bid(0,0,30,0)
			],
		"max_output":70,
		"ramp_up_limit":10,
		"wanted_output": 10,
		"output": 20
		}]
		for test in tests:
			producer = FossilFuelPlant(0,0,test["max_output"],test["ramp_up_limit"])
			producer.setOutput(test["output"])
			producer.receiveOrder(test["orders"])
			self.assertEqual(producer.output, test["wanted_output"])

class TestWindFarm(unittest.TestCase):
	def test_getFutureBid(self):
		tests= [{
		"Producer": WindFarm(12,1,50,Battery(200,200)),
		"predictions":[100,100,100,100],
		"wanted bids": [50,50,50,50]
		}]
		
		for test in tests:
			got = test["Producer"].getFutureBid(test["predictions"])
			got = formatBidList(got)
			self.assertEqual(got,test["wanted bids"],"your future bid did not match the expected")


def formatBidList(bid_list):
	output = []
	for bid in bid_list:
		output.append(bid.amount_electrictiy)
	return output

if __name__ == "__main__":
	unittest.main()
