class Main():
	def __init__(self,distribution,producers):
		self.distribution= distribution
		self.producers = producers
		self.prediction = Prediction()
		self.market = Market()

	def itterate(self):
		time = 0
		while True:
			ussage = self.getUsage(time)
			totalProduction = self.pollProducers()
			
			predictions = self.getPredictions(ussage)
			winners,price = self.maket.getWinners()

			self.sendOrders(winners)
			'''
			[
				[
					[producer,amount],
					[producer,amount]
				],[]]



			{
				producer: [amount,amount.....]
			}
			'''self.distribution.receivePrice(price)


			time += 1

	def getUsage(self,time):
		return self.distribution.ussage(time)

	def pollProducers(self):
		total_energy = 0
		for i in self.producers:
			total_energy += i.current_production
		return total_energy

	def getPredictions(self,ussage):
		return self.prediction.predict(ussage)
	def sendOrders(self,winners):
		for i in self.producers:
			i.receiveOrder(winners[i])



