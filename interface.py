from tkinter import *
import FA as fa

class App(object):
        def __init__(self, master):
                frame = Frame(master, width=1000, height=9000)
                frame.pack()
                self.master = master
                self.ticker = StringVar(frame)
                self.textbox = Entry(frame, textvariable=self.ticker)
                self.button = Button(frame, text="Predict!", fg="blue", command=self.invest)
                
                self.textbox.pack()
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
app.master.title("The Profit Prophet")
root.mainloop()
