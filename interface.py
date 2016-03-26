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
                
                self.name = StringVar()
                self.info = StringVar()
                
                self.name_label = Label(frame, textvariable=self.name, font="Helvetica 32 bold")
                self.info_label = Label(frame, textvariable=self.info)
                
                self.textbox.pack()
                self.button.pack()
                self.name_label.pack()
                self.info_label.pack()
        def invest(self):
                n, r, b, pi, cpps, ppps = fa.company_worth_investing(self.ticker.get())
                self.name.set(n)
                self.info.set("Risk Level: " + r + "\n\n" + \
                "Beta: " + str(b) + "\n\n" + \
                "Price Increase (%): " + str(round(pi*100, 2)) + "%" + "\n\n" + \
                "Current Price per Share: " + str(round(cpps, 2)) + "\n\n" + \
                "Predicted Price per Share: " + str(round(ppps, 2)))

root = Tk()
app = App(root)
app.master.title("The Profit Prophet")
root.mainloop()
