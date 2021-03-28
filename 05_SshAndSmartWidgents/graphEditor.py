import tkinter as tk

class GraphEditor(tk.PanedWindow):
  def __init__(self):
    super().__init__()
    self.pack(fill="both", expand=1)

    self.master.title("GraphEditor")

    self.mode = ""
    self.createLayout()

  def createLayout(self):
    textFrame = tk.LabelFrame(self, text="text editor")
    self.add(textFrame)

    self.text = tk.Text(textFrame, width=40)
    self.text.pack(fill="both", expand=1, padx=2, pady=2)

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

    if self.mode == "move":
      self.canvas.move(self.currentObjId, event.x - self.prevCoords[0],
                                          event.y - self.prevCoords[1])
    elif self.mode == "resize":
      coords = self.canvas.coords(self.currentObjId)
      center = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
      size = (max(10, abs(event.x - center[0])), max(10, abs(event.y - center[1])))
      self.canvas.coords(self.currentObjId, center[0]-size[0], center[1]-size[1],
                                            center[0]+size[0], center[1]+size[1])
    self.prevCoords = (event.x, event.y)

  def canvasOnPress(self, event):
    objs = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if objs:
      self.mode = "move"
      self.currentObjId = objs[0]
    else:
      id = self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, activefill="light gray")
      self.mode = "resize"
      self.currentObjId = id

  def canvasOnRelease(self, event):
    self.mode = ""

GraphEditor().mainloop()