import tkinter as tk
from tkinter.messagebox import showinfo

class MyWidget(tk.Widget):
  def __init__(self, master, widgetType, params, **kwargs):
    widgetType.__init__(self, master, kwargs)
    self.myConfigure(params)

  def myConfigure(self, params):
    l = params.split('/')
    gravity = "NEWS" if len(l) == 1 else l[1]
    l = l[0].split(':')
    rawGridInfo = l
    gridInfo = []
    for l in rawGridInfo:
      l = l.split('+')
      span = 1 if len(l) == 1 else int(l[1]) + 1
      l = l[0].split('.')
      weight = 1 if len(l) == 1 else int(l[1])
      pos = int(l[0])
      gridInfo.append([pos, weight, span])
    self.grid(row =    gridInfo[0][0], rowspan =    gridInfo[0][2],
              column = gridInfo[1][0], columnspan = gridInfo[1][2],
              sticky = gravity)
    self.master.rowconfigure(   gridInfo[0][0], weight=gridInfo[0][1])
    self.master.columnconfigure(gridInfo[1][0], weight=gridInfo[1][1])


  def __getattr__(self, attr):
    def widgetCreator(widgetType, params, **kwargs):
      widget = MyWidget(self, widgetType, params, **kwargs)
      setattr(self, attr, widget)
    return widgetCreator


class Application(tk.Frame):
  def __init__(self, master=None, title="<application>"):
    super().__init__(master)
    self.master.title(title)
    self.master.columnconfigure(0, weight=1)
    self.master.rowconfigure(0, weight=1)
    self.grid(sticky="NEWS")
    self.createWidgets()

  def __getattr__(self, attr):
    def widgetCreator(widgetType, params, **kwargs):
      widget = MyWidget(self, widgetType, params, **kwargs)
      setattr(self, attr, widget)
    return widgetCreator



class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()
