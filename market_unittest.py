from market import *
import unittest
from bid import Bid
from powerstation import Producer

class TestPQ(unittest.TestCase):
	def test_add(self):
		test_queue = PQ()
		test_bids_to_add = [Bid(300,0,200,2),
							Bid(100,0,200,2),
							Bid(200,0,200,2)]
		wanted_results = [300,
						  200,
						  100,]		
		for test in test_bids_to_add:
			test_queue.add(test)
		message = "PQ.add failed"
		
		self.assertEqual(get_amounts_bid(test_queue.q),wanted_results,message)
	def test_dequeue(self):
		test_queue = PQ()
		test_bids_to_add = [[Bid(300,0,200,2),
							Bid(100,0,200,2),
							Bid(200,0,200,2),
							Bid(250,0,200,2)],
							[Bid(315,0,200,2),
							 Bid(200,0,200,2)]]
		wanted_results = [[300],
						  []]
		message = "PQ.dequeue"
		for test in range(len(test_bids_to_add)):
			test_queue.q = []
			for item in test_bids_to_add[test]:
				test_queue.add(item)
			for i in range(3):
				test_queue.dequeue()
			self.assertEqual(get_amounts_bid(test_queue.q),wanted_results[test],message)

class TestMultiLevelQueue(unittest.TestCase):
	def test_add(self):
		test_MLQ = MultiLevelQueue()
		test_bids_to_add =[Bid(300,0,200,1),
							Bid(100,0,200,2),
							Bid(200,0,200,3),
							Bid(250,0,200,5)]
		wanted_result = [[],[300],[100],[200],[],[250]]
		for i in range(len(test_bids_to_add)):
			test_MLQ.add(test_bids_to_add[i])
		for i in range(len(test_MLQ._top_level_list)):
			#print("test_MLQ",get_amounts_bid(test_MLQ._top_level_list[i].q),"wr: ",wanted_result[i])
			self.assertEqual(get_amounts_bid(test_MLQ._top_level_list[i].q),wanted_result[i])

class TestMarket(unittest.TestCase):
	def test_GetWinners(self):
		producers = [Producer(1.3,1,200),
					 Producer(1.6,1,300),
					 Producer(2.4,2,300),
					 Producer(1.4,3,1000)]
		test_market = Market(producers)
		predictions = [500,300,1000]
		winners = test_market.GetWinners(predictions)
		wanted_results = {producers[0]:[Bid(1.3,producers[0],200,1),Bid(1.3,producers[0],200,1),Bid(1.3,producers[0],200,1)],
						  producers[1]:[Bid(1.6,producers[1],300,1),Bid(1.6,producers[1],100,1),Bid(1.6,producers[1],300,1)],
						  producers[2]:["Nothing","Nothing",Bid(2.4,producers[2],300,2)],
						  producers[3]:["Nothing","Nothing",Bid(1.4,producers[3],200,3)],
						  }
		#print(winners,"blip",wanted_results)
		for i in producers:
			#if i in winners:
			#print("winner:",get_amounts_bid(winners[i]))
			#if i  in wanted_results:
			#print("got",get_amounts_bid(winners[i]))
			#print("want",get_amounts_bid(wanted_results[i]))
			self.assertEqual(get_amounts_bid(winners[i]),get_amounts_bid(wanted_results[i]),"oops")



def get_amounts_bid(bid_list):
	formated_list = []
	if bid_list == None:
		return None
	for i in bid_list:
		#print(i.amountBid)
		if i == "Nothing":
			formated_list.append("Nothing")
		else:
			formated_list.append(i.amountBid)
	return formated_list
if __name__ == "__main__":
	#test = TestPQ()
	#test.test_add()
	unittest.main()