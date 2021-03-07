import tkinter as tk
import tkinter.messagebox as msgbox
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

    self.bind('<Configure>', self.resize)

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
    self.rowsNumber = rowsNumber

    self.playButtons = []
    buttonWidth = len(str(rowsNumber * columnsNumber - 1))
    for i in range(1, rowsNumber * columnsNumber):
      playButton = tk.Button(self.playFrame, text=str(i), width=buttonWidth)
      playButton["command"] = lambda button=playButton: self.processClick(button)
      self.playButtons.append(playButton)

    for i in range(rowsNumber):
      self.playFrame.rowconfigure(i, weight=1)

    for i in range(columnsNumber):
      self.playFrame.columnconfigure(i, weight=1)

  def resize(self, ev):
    if (ev.widget == self.playFrame):
      height = ev.height / self.rowsNumber
      width = ev.width / self.columnsNumber
      scale = 0.4 * min(width, height)
      for button in self.playButtons:
        button.config(font=("", int(scale)))

  def processClick(self, button):
    row = button.grid_info()["row"]
    column = button.grid_info()["column"]
    if (abs(self.emptyPos[0] - row) + abs(self.emptyPos[1] - column) == 1):
      button.grid(row=self.emptyPos[0], column=self.emptyPos[1], sticky="NESW")
      self.emptyPos = [row, column]
    if (self.isSolved()):
      msgbox.showinfo(message="You win!!!")
      self.newGame()

  def isSolved(self):
    pos = [0, 0]
    for button in self.playButtons:
      row = button.grid_info()["row"]
      column = button.grid_info()["column"]
      if (pos[0] != row or pos[1] != column):
        return False
      pos[1] += 1
      if (pos[1] == self.columnsNumber):
        pos[0] += 1
        pos[1] = 0
    return True

  def isSolvable(self, order):
    perm = order.copy()
    emptyParity = (len(perm) - perm.index(None) - 1) // self.columnsNumber
    emptyParity = (self.columnsNumber + 1) * emptyParity
    inversions = 0
    perm.remove(None)
    while (len(perm)):
      maxEl = max(perm)
      inversions += len(perm) - perm.index(maxEl) - 1
      perm.remove(maxEl)
    return ((inversions + emptyParity) % 2 == 0)

  def newGame(self):
    order = [i for i in range(len(self.playButtons))]
    order.append(None)
    random.shuffle(order)
    while (not self.isSolvable(order)):
      random.shuffle(order)

    pos = [0, 0]
    for idx in order:
      if (idx == None):
        self.emptyPos = pos.copy()
      else:
        self.playButtons[idx].grid(row=pos[0], column=pos[1], sticky="NESW")
      pos[1] += 1
      if (pos[1] == self.columnsNumber):
        pos[0] += 1
        pos[1] = 0


FifteenGame().mainloop()