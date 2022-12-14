import os
import csv
import sqlite3
import controller.main as main
import gridClasses.substation as substation
import gridClasses.smartmeter as smartmeter
import gridClasses.powerstation as powerstation
import tkinter as tk
import gui

"""simulation is the simulation envirnonment the the main controler runs 
in.

it sets up databases, producers and distribution network and takes in usage
data from a csv. 

"""


class Simulation(object):
    """the simulation class is a class resposnalble for 
    setting up and running main with appropriate data. 
    """

    def __init__(self):
        self._num_meters, self.main_substation = self.generateDistribution()
        producers = self.generateProducers()
        self.setUsages("eirgridData/usage")
        self.setHistory()
        self.controller = main.Main(self._substations[0], producers,self._substations, self._num_meters)
        winners = self.controller.market.GetWinners([5000,0,0,0,0]) # starting production
        self.controller.sendOrders(winners)
        self.results = self.controller.Iterate()

    def setUsages(self, usage_dir):
        """setUsages reads in the passes file path to 
        a csv and creates the aplications database.

        for each usage contained in the passed csv file 
        an entery is entered into the usage database.
        this will be used by the smart meter to return
        its usage to the main controller.
        the time is incremented in .25 because the time
        period of the csv is in 15min and this is a 
        translation of mins to decimal. this is done to
        be consistant with other tables in the aplication.

        Args:
                usage_csv: the filepath to the csv containing
                                        the usage information.
        """
        conn, cursor = self.creatDatabase()
        time_offset = 0
        for file in os.listdir(usage_dir):
            print(file)
            usage_file = open(usage_dir+"/"+file)
            print(usage_dir+"/"+file)
            usage_reader = csv.reader(usage_file)
            next(usage_reader)
            rows = []
            time = 0
            for row in usage_reader:
                self.addRow2DB(cursor, time_offset+time, row)
                time += 0.25
            usage_file.close()
            time_offset += 24.0
        conn.commit()

    def creatDatabase(self):
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS usage")
        cursor.execute("CREATE TABLE usage (decTime TEXT, usage INTEGER)")
        return conn, cursor

    def addRow2DB(self, cursor, time, row):
        # we are deviding by the total usage by the number of
        # smart meteres here because want to get a realistic number.
        # for each smart meter.
        usage_per_meter = int(row[1])//len(self._num_meters)
        cursor.execute("INSERT INTO usage VALUES (?, ?)",
                       (time, usage_per_meter))

    def generateDistribution(self):
        """generates the distribution network.
        creates a substation that the main controler 
        will be connected to. could also create a network of
        substations if modified.
        creates the substation with smart meters connected to it.
        """
        smartmeters = [smartmeter.SmartMeter(), smartmeter.SmartMeter(),smartmeter.SmartMeter(),smartmeter.SmartMeter()]
        second_substation = substation.Substation(0, smartmeters[0:2],[])
        main_substation = substation.Substation(0, smartmeters[2:],[second_substation])
        substations = [main_substation,second_substation]#substation.Substation(0,[],[])

        return smartmeters,substations

    def generateProducers(self):
        """generates a list of producers that the main contoller can use.

        creates producers and appends the to a list.
        """
        producers = []
        producers.append(powerstation.Producer(3.35, 0, 3000))
        producers.append(powerstation.Producer(2.35, 1, 4000))
        producers.append(powerstation.FossilFuelPlant(2.00,1,2000,500))
        producers.append(powerstation.Producer(2.36, 1, 2000))
        battery = powerstation.Battery(2000,1000)
        producers.append(powerstation.WindFarm(2.34,0,2000,battery))
        return producers

    def setHistory(self):
        """sets the inital usage history.
        usage history is important for the prediction module.
        this is to insure there is always usage history available even if it has not
        been running before now.
        it stores the usage history in a database to be accessed by the prediction 
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
            cursor = conn.cursor()
            usage_file = open('eirgridData/initial_prediction.csv')
            usage_reader = csv.reader(usage_file)
            next(usage_reader)
            time = 0
            day = 0
            for row in usage_reader:
                cursor.execute(
                    "INSERT INTO use_history VALUES (?, ?, ?)", (row[1], time, day)
                )
                time += 0.25
                if time == 24:
                    time = 0
                    day += 1
            usage_file.close()
            conn.commit()
    def getResults(self):
        return self.results

if __name__ == "__main__":
    sim = Simulation()
    root = tk.Tk()
    p = gui.GUI(root, sim.controller)
    root.mainloop()
