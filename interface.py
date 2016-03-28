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

# TODO
# 1) Show suggestions when there are multiple matches for a stock in fuzzy searching.
# 2) Color the risk level.


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
            def invest(x):
                self.invest()
            self.textbox.bind('<Return>', invest)

            self.dayn = IntVar(frame)
            self.day_slider = Scale(frame, from_=1, to=30, variable=self.dayn, orient=HORIZONTAL, length=250)

            self.button = Button(frame, text="Predict!", command=self.invest)

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
            self.button.pack()
            self.day_slider.pack()

            info_card.pack(side=LEFT, expand=True)
            self.name_label.pack()
            self.risk_label.pack()
            self.info_label.pack()
            self.info_list.pack(fill=BOTH, expand=True)
            
            f = Figure(figsize=(5,5), dpi=100, facecolor='white')
            self.subplot = f.add_subplot(111)

            canvas = FigureCanvasTkAgg(f, frame)
            canvas.show()
            canvas.get_tk_widget().pack(side=RIGHT, fill=X, expand=True)

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
