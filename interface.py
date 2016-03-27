from tkinter import *
from tkinter_help import *

import FA as fa

import csv
import re

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# TODO: Use Text widget for info_label, instead of Label widget
# 2) SCroll it.
# 3) Show suggestions when there are multiple matches for a stock in fuzzy searching.


with open('cboesymboldir2.csv', mode='r') as in_file:
    reader = csv.DictReader(in_file)
    ticker_to_name_dict = {row['Stock Symbol']: row['Company Name'] for row in reader}
    name_to_ticker_dict = {v.lower(): k for (k, v) in ticker_to_name_dict.items()}

def name_to_ticker(n):
    for (k, v) in name_to_ticker_dict.items():
        if n in k or n in v.lower() or k in n:
            return v
        
class App(object):
        def __init__(self, master):
            frame = Frame(master, width=1850, height=900)
            frame.pack(expand=False)
            self.master = master
            
            self.ticker = StringVar(frame)
            self.textbox = Entry(frame, textvariable=self.ticker, width=300)

            self.dayn = IntVar(frame)
            self.day_slider = Scale(frame, from_=1, to=30, variable=self.dayn, orient=HORIZONTAL, length=250)

            self.button = Button(frame, text="Predict!", bg="blue", command=self.invest)

            info_card = VerticalScrolledFrame(frame, width=925, height=900)
            self.name = StringVar(info_card)
            self.info = StringVar(info_card)

            self.name_label = Label(info_card.interior, textvariable=self.name, font="Helvetica 32 bold")
            self.info_label = Label(info_card.interior, textvariable=self.info)
            
            self.textbox.pack()
            self.day_slider.pack()
            self.button.pack()

            info_card.pack(side=LEFT)
            self.name_label.pack()
            self.info_label.pack()
            
            f = Figure(figsize=(5,5), dpi=100, facecolor='white')
            self.subplot = f.add_subplot(111)

            canvas = FigureCanvasTkAgg(f, frame)
            canvas.show()
            canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

        def invest(self):
            ticker = self.ticker.get() in ticker_to_name_dict
            print(ticker)
            if self.ticker.get() in ticker_to_name_dict:
                predictions = fa.company_worth_investing(self.ticker.get(), iters=self.dayn.get())
            else:
                print(name_to_ticker(self.ticker.get().lower()))
                predictions = fa.company_worth_investing(name_to_ticker(self.ticker.get().lower()), iters=self.dayn.get())

            if predictions != None:
                n = ""
                if ticker:
                    n = self.ticker.get()
                else:
                    n = name_to_ticker(self.ticker.get().lower())
                    
                vs = list(map(eval, fa.get_company_info(n)['history'])) + list(map(lambda x: x[5], predictions))
                self.subplot.cla()
                self.subplot.plot(vs)
                
            if predictions == None:
                self.name.set("Company '"+self.ticker.get()+"' not found.")
                self.info.set("")
                self.subplot.cla()
            else:
                n, r, b, pi, cpps, ppps = predictions[-1]
                self.name.set("\n"+ticker_to_name_dict[n].title()
                                .replace("Stk", "").replace(" Com", "") + " ("+n+") \n")
                self.info.set("Risk Level: " + r.upper() + "\n" +\
                                "Current Price per Share: " + str(round(cpps, 2)) + "\n" + \
                                "Beta: " + str(b) + "\n\n\n")

                for n, r, b, pi, cpps, ppps in predictions:
                    self.info.set(self.info.get()+\
                                    "Price Increase (%): " + str(round(pi*100, 2)) + "%" + "\n" + \
                                    "Predicted Price per Share: " + str(round(ppps, 2)) + "\n\n")

root = Tk()
root.geometry('{}x{}'.format(1850, 900))

app = App(root)
app.master.title("The Profit Prophet")

root.mainloop()
