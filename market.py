from bid import Bid
"""This is the Market module used to decide what producers can produce electricity.
	
	The Market mondule is used to decide what producers have the controlers authority
	to meet the predicted future demand. The market module will take the predicted demand
	and request from each producer an amout of electricity they can produce and the price
	that they can produce it at. it then sorts it into a multilevel queue based on how
	environmentaly frendly each source is and picks the most least expensive most green
	energy source. The Market class is the only public class.

	Typical usage example:
		market = Market(producers)
		winners = market.GetWinners(predictions)

"""

class Market(object):
	"""The market class is the main class that holds the public meathod GetWinners that 
	will be called by the main module.

	Once get winners is called it requests the bids from the producers and then selects
	the winning bids for each time

	Args:
		producers: a list of all the producers class

	"""
	def __init__(self, producers):
		self._producers = producers
	def GetWinners(self,predictions):
		""" Gets the winning bids from the producers based on the predictions passed.
			
			Gets the bids from all of the producers set on initialisation then askes
			these producers for bids for the power usage predictions passed and then 
			returns the winners
		Args:
			predictions: a list of predictions for the energy usage in 15 min increments
		Returns:
			winners: a dictionary with the format 
					{<producer_object>: [<bid_object>,<bid_object>.....]} 

		"""
		bids_by_time = self.requestBids(predictions)
		winners = self.selectWinners(predictions,bids_by_time)
		return winners

	def requestBids(self,predictions):
		"""requests bids from all the producers

		requests the bids from all the producers and puts them in a multilevel queue
		based on how green the energy source is

		Args:
			predictions: a list of predictions for the energy usage in 15 min increments
		Returns:
			 bidding_rankings_by_time: a list containing multilevel priority queues based on how green the
			 energy source is. the top level queue is ordered on greeness and the sub
			 queues are ordered on the price.
		"""
		bidding_rankings_by_time = []
		for i in predictions:
			bidding_rankings_by_time.append(MultiLevelQueue())
		for producer in self._producers:
			for i,bid in ennumerate(producer.GetFutureBid(predictions)):
				bidding_rankings_by_time[i].add(bid)
		return bidding_rankings_by_time
	def selectWinners(self,predictions,bids_by_time):
		"""

		Args:
			predictions: a list of predictions for the energy usage in 15 min increments

			bids_by_time: a list of multilevel priority queues based on how green the
			 energy source is. the top level queue is ordered on greeness and the sub
			 queues are ordered on the price.
		Returns:
			winners: a dictionary with the format 
					{<producer_object>: [<bid_object>,<bid_object>.....]} 
		"""

		winners = {}
		for i,time in enumerate(bids_by_time):
			winners = time.selectWinners(predictions[i],winners)


class MultiLevelQueue(object):
	""" a multilevel priority queue

		a list of queues each queue being organised on priority of the bids ammount
		in money and being put in each queue by its environmental rating

	"""
	def __init__(self):
		self._top_level_list = []
	def add(self,bid):
		level = bid.level
		# if the level does not exist yet in the MLQ add it and all precieding levels
		if level < len(self._top_level_list):
			for i in range((level+1)-len(self._top_level_list)):
				self._top_level_list.append(PriorityQueue())
		self._top_level_list[level].add()
	def selectWinners(self,prediction,winners):
		"""
		selects the winners of the bidding by 
		dequeing the priority queue
		"""
		total = prediction
		for level in self._top_level_list:
			winner = selected.dequeue
			if winner == None:
				continue
			total -= winner.amount_electrictiy
			# making sure the order does not contain more production than necicary
			if total <0:
				winner.amount_electrictiy+= total
				total = 0
			winners[winner.producer].append(winner)
			if total ==0:
				#making sure the output format is as expected
				for producer in winners.keys():
					if len(winners[producer])< winners[winner.producer]:
						producer.append(None)
		return winners 


class PQ(object):
	def __init__(self):
		self.q = []
	def add(self,bid):
		# queuing elements from the lists end to reduce memory realocation on dequeue
		for i in range(len(self.q)-1,0,-1):
			if self.q[i] > bid.amountBid:
				if i == len(self.q)-1:
					self.q.append(bid)
					return
				self.q.insert(i+1,bid)
				return
		self.q.insert(0,bid)
	def dequeue(self):
		# checking if the list is not empty and then poping
		if self.q:
			return self.q.pop()
		return None

