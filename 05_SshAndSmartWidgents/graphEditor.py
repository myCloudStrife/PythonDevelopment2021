import tkinter as tk
import os

class GraphEditor(tk.PanedWindow):
  def __init__(self):
    super().__init__()
    self.pack(fill="both", expand=1)

    self.master.title("GraphEditor")

    self.mode = ""
    self.objIds = []
    self.createLayout()

  def createLayout(self):
    textFrame = tk.LabelFrame(self, text="text editor")
    self.add(textFrame)

    self.text = tk.Text(textFrame, width=40, undo=True, wrap="word")
    self.text.pack(fill="both", expand=1, padx=2, pady=2)
    self.text.tag_config("error", background="red")
    self.text.bind("<Any-KeyPress>", lambda event: self.master.after(100, self.processText))

    graphicsFrame = tk.Frame(self)
    self.add(graphicsFrame)

    graphicsMenuFrame = tk.Frame(graphicsFrame)
    graphicsMenuFrame.pack(side="top", fill="x")
    tk.Variable()
    self.canvasCoord = tk.StringVar(self, value="(0:0)")
    tk.Label(graphicsMenuFrame, textvariable=self.canvasCoord).pack(side="right")
    canvasFrame = tk.LabelFrame(graphicsFrame, text="canvas")
    canvasFrame.pack(side="top", fill="both", expand=1)
    self.canvas = tk.Canvas(canvasFrame, bg='white')
    self.canvas.pack(fill="both", expand=1)
    self.canvas.bind("<Motion>", self.canvasOnMove)
    self.canvas.bind("<Button>", self.canvasOnPress)
    self.canvas.bind("<ButtonRelease>", self.canvasOnRelease)


  def canvasOnMove(self, event):
    self.canvasCoord.set(f"({event.x}:{event.y})")

    if self.mode != "":
      if self.mode == "move":
        self.canvas.move(self.currentObjId, event.x - self.prevCoords[0],
                                            event.y - self.prevCoords[1])
      elif self.mode == "resize":
        coords = self.canvas.coords(self.currentObjId)
        center = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
        size = (max(10, abs(event.x - center[0])), max(10, abs(event.y - center[1])))
        self.canvas.coords(self.currentObjId, center[0]-size[0], center[1]-size[1],
                                              center[0]+size[0], center[1]+size[1])
      line = self.objIds.index(self.currentObjId) + 1
      command = self.text.get(f"{line}.0", f"{line}.0 + 1 line")
      coords = self.canvas.coords(self.currentObjId)
      command = command.split()
      command[1:5] = [str(coord) for coord in coords]
      self.text.replace(f"{line}.0", f"{line}.0 + 1 line - 1 char", " ".join(command))

    self.prevCoords = (event.x, event.y)

  def canvasOnPress(self, event):
    #find doesn't work for objects with empty fill
    objs = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if objs:
      self.mode = "move"
      self.currentObjId = objs[-1]
    else:
      command = (f"oval {event.x-10} {event.y-10} {event.x+10} {event.y+10} "
                  "width=1 outline=\"black\" fill=\"white\"")
      id = self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10,
                                   width=1, outline="black", fill="white", activefill="light gray")
      self.mode = "resize"
      self.currentObjId = id
      line = len(self.objIds) + 1
      if (line > 1):
        command = os.linesep + command
      self.text.insert("end", command)
      self.objIds.append(id)

  def canvasOnRelease(self, event):
    self.mode = ""

  def processText(self):
    self.text.tag_remove("error", "1.0", "end")
    commands = self.text.get("1.0", "end").split(os.linesep)[0:-1]
    for line, command in enumerate(commands, 1):
      if len(self.objIds) < line:
        self.objIds.append(None)
      try:
        self.canvas.delete(self.objIds[line - 1])
        name, *parameters = command.split()
        id = eval(f"self.canvas.create_{name}({','.join(parameters)}, activefill=\"light gray\")")
        self.objIds[line - 1] = id
      except:
        self.text.tag_add("error", f"{line}.0", f"{line}.0 + 1 line")

    if len(commands) < len(self.objIds):
      for id in self.objIds[len(commands):]:
        self.canvas.delete(id)
      self.objIds = self.objIds[:len(commands)]


GraphEditor().mainloop()