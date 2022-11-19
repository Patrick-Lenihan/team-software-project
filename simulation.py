import csv
import sqlite3
import main
import substation
import smartmeter
import powerstation
"""simulation is the simulation envirnonment the the main controler runs 
in.

it sets up databases, producers and distribution network and takes in ussage
data from a csv. 

"""
class Simulation(object):
	"""the simulation class is a class resposnalble for 
	setting up and running main with appropriate data. 
	"""
	def __init__(self):
		self._num_meters, self._main_substation = self.generateDistribution()
		producers = self.generateProducers()
		self.setUsages("ussage.csv")
		self.setHistory()
		contoler = main.Main(self._main_substation,producers)
		contoler.Iterate()
	def setUsages(self,ussage_csv):
		"""setUsages reads in the passes file path to 
		a csv and creates the aplications database.

		for each usage contained in the passed csv file 
		an entery is entered into the ussage database.
		this will be used by the smart meter to return
		its ussage to the main controller.
		the time is incremented in .25 because the time
		period of the csv is in 15min and this is a 
		translation of mins to decimal. this is done to
		be consistant with other tables in the aplication.

		Args:
			ussage_csv: the filepath to the csv containing
						the ussage information.
		"""
		conn, cursor = self.creatDatabase()
		ussage_file= open(ussage_csv)
		ussage_reader = csv.reader(ussage_file)
		next(ussage_reader)
		rows = []
		time = 0 
		for row in ussage_reader:
			self.addRow2DB(cursor,time,row)
			time += 0.25
		ussage_file.close()
		conn.commit()
	def creatDatabase(self):
		conn = sqlite3.connect("app.db")
		cursor = conn.cursor()
		cursor.execute("DROP TABLE IF EXISTS ussage")
		cursor.execute("CREATE TABLE ussage (decTime TEXT, ussage INTEGER)")
		return conn, cursor
	def addRow2DB(self,cursor,time,row):
		# we are deviding by the total ussage by the number of 
		# smart meteres here because want to get a realistic number.
		# for each smart meter.
		usage_per_meter = int(row[1])//self._num_meters
		cursor.execute("INSERT INTO ussage VALUES (?, ?)",(time,usage_per_meter))
	def generateDistribution(self):
		"""generates the distribution network.
		creates a substation that the main controler 
		will be connected to. could also create a network of
		substations if modified.
		creates the substation with smart meters connected to it.
		"""
		smartmeter_list = [smartmeter.SmartMeter(0),smartmeter.SmartMeter(0)]
		main_substation = substation.Substation(0,smartmeter_list)

		return len(smartmeter_list), main_substation
	def generateProducers(self):
		"""generates a list of producers that the main contoller can use.

		creates producers and appends the to a list.
		"""
		producers = []
		producers.append(powerstation.Producer(3.35,0,3000))
		producers.append(powerstation.Producer(2.35,1,4000))
		return producers
	def setHistory(self):
		"""sets the inital ussage history.
		ussage history is importent for the prediction module.
		this is to insure there is always usage history available even if it has not
		been running before now.
		it stores the ussage history in a database to be accessed by the prediction 
		module.
		"""
		conn = sqlite3.connect('app.db')
		with conn:
			conn.execute("""DROP TABLE IF EXISTS use_history;""")
			conn.execute("""
				CREATE TABLE use_history
				(
					use FLOAT,
					time FLOAT,
					day INTEGER
					);""")
			for i in range(5):# days
				for j in range(24): # hours
					for k in range(4):
						conn.execute('''INSERT INTO use_history (use, time, day) VALUES (%d*96+%d*4+%d, %f, %d)'''%(i,j,k,j+k*.25,i))

if __name__ == "__main__":
	sim = Simulation()

