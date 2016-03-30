from tkinter import *

import FA as fa

import csv
import re
import numpy as np
from fuzzywuzzy import process

import matplotlib
matplotlib.use("TkAgg")

from matplotlib import collections as mc
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

with open('cboesymboldir2.csv', mode='r') as in_file:
    reader = csv.DictReader(in_file)
    ticker_to_name_dict = {row['Stock Symbol']: row['Company Name'] for row in reader}
    name_to_ticker_dict = {v.lower(): k for (k, v) in ticker_to_name_dict.items()}

def name_to_ticker(n):
    choices = list(map(lambda x: x.replace("inc.", ""), name_to_ticker_dict.keys()))
    k = process.extractOne(n, choices)[0]
    return name_to_ticker_dict[k.replace("  ", " inc. ")]

class App(object):
        def __init__(self, master):
            frame = Frame(master, width=1850, height=900)
            frame.pack(expand=False)
            self.master = master
            
            self.ticker = StringVar(frame)
            self.textbox = Entry(frame, textvariable=self.ticker, width=300)
            def invest(x):
                self.invest()
            self.textbox.bind('<Return>', invest)

            self.dayn = IntVar(frame)
            self.day_slider = Scale(frame, from_=1, to=30, variable=self.dayn, orient=HORIZONTAL, length=250)

            self.button = Button(frame, text="Predict!", command=self.invest, relief=RAISED, padx=8, pady=5)

            info_card = Frame(frame)
            self.name = StringVar(info_card)
            self.info = StringVar(info_card)
            self.risk = StringVar(info_card)

            self.name_label = Label(info_card, textvariable=self.name, font="Helvetica 32 bold")
            self.risk_label = Label(info_card, textvariable=self.risk, font="Helvetica 16", fg="green")
            self.info_label = Label(info_card, textvariable=self.info, font="Helvetica 16", fg="darkgray")

            scrollbar = Scrollbar(info_card)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.info_list  = Listbox(info_card, yscrollcommand=scrollbar.set, borderwidth=0)
            scrollbar.config(command=self.info_list.yview)
            
            self.textbox.pack()
            self.textbox.focus_set()
            self.day_slider.pack()
            self.button.pack()

            info_card.pack(side=LEFT, expand=True)
            self.name_label.pack()
            self.risk_label.pack()
            self.info_label.pack()
            self.info_list.pack(fill=BOTH, expand=True)
            
            self.fig = plt.figure()
            
            rect = self.fig.patch
            rect.set_facecolor('white')
            
            self.subplot = self.fig.add_subplot(1, 1, 1)
            
            self.fig.suptitle('Share Price History')

            canvas = FigureCanvasTkAgg(self.fig, frame)
            canvas.show()
            canvas.get_tk_widget().pack(side=RIGHT, fill=X, expand=True)

        def invest(self):
            ticker = self.ticker.get() in ticker_to_name_dict
            if self.ticker.get() in ticker_to_name_dict:
                predictions = fa.company_worth_investing(self.ticker.get(), iters=self.dayn.get())
            else:
                predictions = fa.company_worth_investing(name_to_ticker(self.ticker.get().lower()), iters=self.dayn.get())

            if predictions != None:
                n = ""
                if ticker:
                    n = self.ticker.get()
                else:
                    n = name_to_ticker(self.ticker.get().lower())
                info = fa.get_company_info(n)
                
                real = list(map(eval, info['history'])) + [info['Current']]
                pred = list(map(lambda x: x[5], predictions))
                
                self.subplot.cla()
                self.subplot.plot(real + pred, zorder=1)
                
                x = range(len(real+pred))
                y = real+pred
                print(len(real), " and ", len(pred))
                
                def choose_color(i):
                    if i >= len(real):
                        return '#ff0000'
                    else:
                        return '#0000ff'
                    
                c = [choose_color(i) for i in x]
                self.subplot.scatter(x, y, c=c, s=12, zorder=2, edgecolor='white')
                
                self.subplot.set_xlim([0, len(real+pred)])
                
            if predictions == None:
                self.name.set("Company '"+self.ticker.get()+"' not found.")
                self.info.set("")
                self.subplot.cla()
            else:
                n, r, b, pi, cpps, ppps = predictions[-1]
                self.name.set("\n"+ticker_to_name_dict[n].title()
                                .replace("Stk", "").replace(" Common Stock", "").replace(" Com", "") + " ("+n+") \n")
                self.risk.set("Risk Level: " + r.upper() + "\n")
                if r == 'low':
                    self.risk_label.config(fg="green")
                elif r == 'medium':
                    self.risk_label.config(fg="#CCCC00")
                elif r == 'high':
                    self.risk_label.config(fg="red")
                    
                self.info.set("Current Price per Share: $" + str(round(cpps, 2)) + "\n" + \
                              "Beta: " + str(b) + "\n\n\n")

                self.info_list.delete(0, END)
                for n, r, b, pi, cpps, ppps in predictions:
                    self.info_list.insert(END, "Increase: " + str(round(pi*100, 2)) + "%" + ", " + \
                                               "Predicted Price: $" + str(round(ppps, 2)) + "\n\n")

root = Tk()
root.geometry('{}x{}'.format(1850, 900))

app = App(root)
app.master.title("The Profit Prophet")

root.mainloop()
