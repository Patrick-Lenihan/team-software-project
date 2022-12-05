import tkinter as tk
import tkinter.ttk as ttk
from gridClasses import powerstation, smartmeter, substation
import eirgridData
import simulation
import controller.main as main
import sqlite3

class GUI():
    ''' '''

    #CONSTRUCTOR
    def __init__(self, root):
        #ROOT
        self.root = root
        self.root.title('Controller GUI')
        self.root.geometry('1000x650')
        self.root.configure(background = 'white')

        #FRAMES
        frame = tk.Frame(root)

        self.mainAreaFrame = tk.Frame(self.root)
        
        self.rightFrame = tk.Frame(self.root)
        self.rightFrame = tk.Frame(self.root, bg = '#7C90A0')
        self.rightFrame.place(x = 735, y = 0, width = 250, height = 620)
        welcome = tk.Text(self.rightFrame, height = 2, width = 20, font = 'calibri', bg = '#7C90A0', highlightthickness=0, highlightbackground = '#7C90A0', highlightcolor = '#7C90A0', relief = 'flat')
        welcome.insert(tk.END, 'Select a grid element for more information')
         
        self.mainAreaFrame = tk.Frame(self.root, bg = '#181D27')
        self.mainAreaFrame.place(x = 10, y = 0, width = 700, height = 620)

        #RIGHT FRAME ACTIONS - DISPLAY BUTTONS IN RIGHT FRAME + THEIR ACTIONS
        '''def substationDisplay(self = self):
            for widget in self.rightFrame.winfo_children():
                if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                    widget.grid_remove()
            
            substationText = tk.Label(self.rightFrame, text = 'Substation', font = 'calibri')
            substationText.grid(row = 0, column = 0, pady = 10)
            usageByTime = tk.Button(self.rightFrame, text = 'Daily usage by \n connected homes ????', font = 'calibri', width = 28, bg ='#52FFB8', relief = 'flat', command = lambda: open_popup('Total Energy Usage by Time', data = allHomesUsage()))
            usageByTime.grid(row = 1, column = 0, pady = 20, padx = 10)

            def dailyTotalHomeUsage():
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()

                for row in cur.execute('SELECT * FROM ')'''
                    

        def smartMeterDisplay(self = self):
            for widget in self.rightFrame.winfo_children():
               if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                    widget.grid_remove()

            smartMeterText = tk.Label(self.rightFrame, text = 'Smart Meter', font = 'calibri')
            smartMeterText.grid(row = 0, column = 0, pady = 10)
            smartMeterUsage = tk.Button(self.rightFrame, text = 'Total energy usage by \n connected houses \n with a smart meter', 
                font = 'calibri', width = 28, bg = '#52FFB8', relief = 'flat', command = lambda: totalHomeUsage())
            smartMeterUsage.grid(row = 1, column = 0, pady = 20, padx = 10)

            def totalHomeUsage():
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()
                rows = []

                for row in cur.execute('SELECT * FROM use_history;'):
                    print(row)
                    rows.append(row)

                #total day usage
                total_day = 0
                daily = []

                for r in rows:
                    if r[1] < 23.75:
                        total_day += int(r[0])
                    else:
                        daily.append(total_day)
                        total_day = 0
                
                top = tk.Toplevel(root)
                top.geometry('750x500')
                top.configure(background = '#181D27')
                day = tk.Text(top, width = 100, font = 'Calibri', fg = 'white', bg = '#181D27', relief = 'flat')
                day.insert(tk.END, 'Total daily energy usage by connected households: \n ')
                for d in daily:
                    day.insert(tk.END, str(d) + '\n')
                day.pack()

        def BESSDisplay(self = self):
            for widget in self.rightFrame.winfo_children():
                if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                    widget.grid_remove()
            
            BESSText = tk.Label(self.rightFrame, text = 'BESS - Battery \n Energy Storage System', font = 'calibri')
            BESSText.grid(row = 0, column = 0, pady = 10)
            dischargeBattery = tk.Button(self.rightFrame, text = 'Discharge battery', font = 'calibri', width = 28, bg = '#52FFB8', relief = 'flat', command = lambda: open_popup('Discharge Battery'))
            dischargeBattery.grid(row = 1, column = 0, pady = 20, padx = 10)
           
        def productionDisplay(self = self):
            for widget in self.rightFrame.winfo_children():
                if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                    widget.grid_remove()

            productionText = tk.Label(self.rightFrame, text = 'Production levels', font = 'calibri')
            productionText.grid(row = 0, column = 0, pady = 10)
            checkProduction = tk.Button(self.rightFrame, text = 'Check production levels \n by all producers', font = 'calibri', width = 28, bg = '#52FFB8', relief = 'flat', command = lambda: checkProductionLevels())         
            checkProduction.grid(row = 1, column = 0, pady = 20, padx = 10)

            def checkProductionLevels():
                level = main.Main.pollProducers(main)

                top = tk.Toplevel(root)
                top.geometry('750x500')
                top.configure(background = '#181D27')
                data = tk.Text(top, width = 100, font = 'Calibri', fg = 'white', bg = '#181D27', relief = 'flat')
                data.insert(tk.END, 'Current production levels \n')
                for item in level:
                    data.insert(tk.END, str(item) + '\n')
                data.pack()

        def open_popup(define_title, data): #where define_title is the window title and data is the content to be displayed
            '''
            Reusable function for opening a popup window when user
            clicks on a button in the rightFrame. 
        
            Args:
            define_title: Set a title for the popup window
            '''
            top = tk.Toplevel(root)
            top.geometry('750x500')
            top.title(define_title)
            top.configure(background = '#181D27')

            data.grid(top)


        #MAIN AREA BUTTONS
        production = tk.Button(self.mainAreaFrame, text = 'Production', font = 'calibri', width = 15, bg ='#52FFB8', relief = 'flat', command = lambda: productionDisplay())
        production.grid(row = 1, column = 0, pady = 100, padx = 20)
        smartMeter = tk.Button(self.mainAreaFrame, text = 'Smart meter', font = 'calibri', width = 10, bg ='#52FFB8', relief = 'flat', command = lambda: smartMeterDisplay(self = self))
        smartMeter.grid(row = 1, column = 1, pady = 100, padx = 10)
        bess = tk.Button(self.mainAreaFrame, text = 'BESS', font = 'calibri', width = 10, bg ='#52FFB8', relief = 'flat', command = lambda: BESSDisplay(self = self))
        bess.grid(row = 1, column = 2, pady = 100, padx = 10)
        
        controller = tk.Button(self.mainAreaFrame, text = 'Controller', font = 'calibri', width = 15, bg ='white', relief = 'flat', state = 'disabled')
        controller.grid(row = 13, column = 1, pady = 20)