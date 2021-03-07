import tkinter as tk
import random


class FifteenGame(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Game of 15")
    self.columnconfigure(0, weight=1)

    self.rowconfigure(0, weight=0)
    self.createMenuFrame()

    self.rowconfigure(1, weight=1)
    self.createPlayFrame()

    self.newGame()

  def createMenuFrame(self):
    self.menuFrame = tk.Frame(self)
    self.menuFrame.grid(row=0, column=0, sticky="EW")

    self.newButton = tk.Button(self.menuFrame, text="New", command=self.newGame)
    self.newButton.grid(row=0, column=0)
    self.menuFrame.columnconfigure(0, weight=1)

    self.exitButton = tk.Button(self.menuFrame, text="Exit", command=self.quit)
    self.exitButton.grid(row=0, column=1)
    self.menuFrame.columnconfigure(1, weight=1)

  def createPlayFrame(self):
    self.playFrame = tk.Frame(self)
    self.playFrame.grid(row=1, column=0, sticky="NESW")

    rowsNumber = columnsNumber = 4
    self.columnsNumber = columnsNumber

    self.playButtons = []
    for i in range(1, rowsNumber * columnsNumber):
      playButton = tk.Button(self.playFrame, text=str(i))
      playButton["command"] = lambda: self.processClick(playButton)
      self.playButtons.append(playButton)

    for i in range(rowsNumber):
      self.playFrame.rowconfigure(i, weight=1)

    for i in range(columnsNumber):
      self.playFrame.columnconfigure(i, weight=1)


  def processClick(self, button):
    pass

  def newGame(self):
    order = [i for i in range(len(self.playButtons))]
    order.append(None)
    random.shuffle(order)
    #todo: check solvability

    pos = [0, 0]
    for idx in order:
      if (idx == None):
        self.emptyPos = pos
      else:
        self.playButtons[idx].grid(row=pos[0], column=pos[1], sticky="NESW")
      pos[1] += 1
      if (pos[1] == self.columnsNumber):
        pos[0] += 1
        pos[1] = 0


FifteenGame().mainloop()