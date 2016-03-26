from tkinter import *
import FA as fa

class App(object):
	def __init__(self, master):
		frame = Frame(master, width=800, height=900)
		frame.pack()
		self.ticker = StringVar(master)
		self.textbox = Entry(master, relief=SUNKEN, textvariable=self.ticker)
		self.textbox.pack()
		self.button = Button(frame, text="Predict!", fg="blue",
                                     anchor=S, command=self.invest,
                                     relief=RAISED)
		self.button.pack()
	def invest(self):
		n, r, b, pi, cpps, ppps = fa.company_worth_investing(self.ticker.get())
		

root = Tk()
app = App(root)
root.mainloop()
