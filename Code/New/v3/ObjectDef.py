from VOBJ import createVector
from GuiHitboxOBJ import GUI_REGION


class Object(GUI_REGION):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.pos = createVector(x, y)
		self.dimensions = createVector(w, h)

		self.mouseReference = (0, 0)