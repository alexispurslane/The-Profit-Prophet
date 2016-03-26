from tkinter import *
import FA as fa

class App(object):
        def __init__(self, master):
                frame = Frame(master, width=1000, height=9000)
                frame.pack()
                self.ticker = StringVar(master)
                self.textbox = Entry(master, relief=SUNKEN, textvariable=self.ticker)
                self.textbox.pack()
                self.button = Button(frame, text="Predict!", fg="blue", command=self.invest,
                                     relief=RAISED, side=BOTTOM)
                self.button.pack()
        def invest(self):
                n, r, b, pi, cpps, ppps = fa.company_worth_investing(self.ticker.get())
                print("Name: " + n)
                print("Risk Level: " + r)
                print("Beta: " + str(b))
                print("Price Increase: " + str(round(pi*100, 2)) + "%")
                print("Current Price per Share: " + str(round(cpps, 2)))
                print("Predicted Price per Share: " + str(round(ppps, 2)))

root = Tk()
app = App(root)
app.master.title = "The Profit Prophet"
root.mainloop()
