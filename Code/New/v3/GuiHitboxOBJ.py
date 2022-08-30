from VOBJ import createVector

class GUI_REGION:
	def __init__(self, x, y, w, h):
		self.HB_pos = createVector(x, y)
		self.HB_dim = createVector(w, h)

	def IN_COLLISION_CHECK(self, mVec):
		if mVec[0] > self.HB_pos.x - 2 and mVec[0] < self.HB_pos.x + self.HB_dim.x + 2:
			if mVec[1] > self.HB_pos.y - 10 and mVec[1] < self.HB_pos.y + self.HB_dim.y + 2:
				# mouseRelativeToBox = createVector(mVec[0] - self.HB_pos.x, mVec[1] - self.HB_pos.y)
				return True
		return False