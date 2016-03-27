from tkinter import *
import FA as fa
import csv

with open('cboesymboldir2.csv', mode='r') as in_file:
    reader = csv.DictReader(in_file)
    ticker_to_name_dict = {row['Stock Symbol']: row['Company Name'] for row in reader}
    name_to_ticker_dict = {v.lower(): k for (k, v) in ticker_to_name_dict.items()}

def name_to_ticker(n):
    for (k, v) in name_to_ticker_dict.items():
        if n in k or n in v or k in n or v in n:
            return v
    
class App(object):
        def __init__(self, master):
                frame = Frame(master, width=1000, height=9000)
                frame.pack()
                self.master = master
                
                self.ticker = StringVar(frame)
                self.textbox = Entry(frame, textvariable=self.ticker)
                
                self.dayn = StringVar(frame)
                self.days = Entry(frame, textvariable=self.dayn)
                
                self.button = Button(frame, text="Predict!", fg="blue", command=self.invest)
                
                self.name = StringVar()
                self.info = StringVar()
                
                self.name_label = Label(frame, textvariable=self.name, font="Helvetica 32 bold")
                self.info_label = Label(frame, textvariable=self.info)
                
                self.textbox.pack()
                self.days.pack()
                self.button.pack()
                self.name_label.pack(side=LEFT)
                self.info_label.pack(side=LEFT)
                
        def invest(self):
                if self.ticker.get() in ticker_to_name_dict:
                    predictions = fa.company_worth_investing(self.ticker.get(), iters=eval(self.dayn.get()))
                else:
                    predictions = fa.company_worth_investing(name_to_ticker(self.ticker.get().lower()), iters=eval(self.dayn.get()))
                    
                n, r, b, pi, cpps, ppps = predictions[-1]
                self.name.set("\n"+ticker_to_name_dict[n].title()
                                .replace("Stk", "").replace(" Com", "") + " ("+n+") ")
                self.info.set("Risk Level: " + r.upper() + "\n" +\
                              "Current Price per Share: " + str(round(cpps, 2)) + "\n" + \
                              "Beta: " + str(b) + "\n\n\n")
                
                for n, r, b, pi, cpps, ppps in predictions:
                    self.info.set(self.info.get()+\
                    "Price Increase (%): " + str(round(pi*100, 2)) + "%" + "\n" + \
                    "Predicted Price per Share: " + str(round(ppps, 2)) + "\n\n")

root = Tk()
app = App(root)
app.master.title("The Profit Prophet")
root.mainloop()
