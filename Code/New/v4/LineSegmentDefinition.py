from random import randint


class lineSeg:
	def __init__(self, x1, y1, x2, y2, orientation, col=(0, 0, 0)):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.col = col
		self.orientation = orientation

	def isSharedPoint(self, otherLineSeg):
		"""
		Function to calculate if two line segments share a coordinate and then returns the coordinates of
		the new longer line. Vertical is just x,y flip of horizontal.
		"""
		if self.orientation != otherLineSeg.orientation: return False  # Check for same orientation

		if self.orientation == 'H':  # Handle horizontal lines
			if {self.y1, self.y2} == {otherLineSeg.y1, otherLineSeg.y2}:  # check if all y coords are the same using sets

				if max(self.x1, self.x2) != min(otherLineSeg.x1, otherLineSeg.x2): return False  # make sure line is adding to current

				if {self.x1, self.x2} & {otherLineSeg.x1, otherLineSeg.x2}:  # check for shared point using bitwise and on a set
					# new line segment is min of self, max of other
					return lineSeg(self.x1, self.y1, otherLineSeg.x2, self.y1, self.orientation, (randint(0, 254), randint(0, 254), randint(0, 254)))

				else: return False
			else: return False

		else:  # Handle vertical lines
			if {self.x1, self.x2} == {otherLineSeg.x1, otherLineSeg.x2}:  # check if all x coords are the same using sets

				if max(self.y1, self.y2) != min(otherLineSeg.y1, otherLineSeg.y2): return False  # make sure line is adding to current

				if {self.y1, self.y2} & {otherLineSeg.y1, otherLineSeg.y2}:  # check for shared point using bitwise and on a set
					# new line segment is min of self, max of other
					return lineSeg(self.x1, self.y1, self.x1, otherLineSeg.y2, self.orientation, (randint(0, 254), randint(0, 254), randint(0, 254)))

				else:
					return False
			else:
				return False

	def __repr__(self):
		return f'({self.x1}, {self.y1}) => ({self.x2}, {self.y2})'
