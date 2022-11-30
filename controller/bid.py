class Bid(object):
	"""Bid is the class that is used to represent a bid from a producer to the marked

		it will be passed from the prucer class to the market class and then back to the 
		producer class by the main module.

		Args:
			bid: is the amount of money bid per unit of electricity
			producer: is the producer that is bidding the amount
			amount_electricity: is the maximum amount of electricity that is being offered
			level: is the environmental rating of the energy source. 
		"""
	def __init__(self,bid,producer,amount_electrictiy,level):
		self.amountBid = bid
		self.producer = producer
		self.amount_electrictiy = amount_electrictiy
		self.level = level

	def repr(self):
		return "bid: "+str(self.amount_electrictiy)