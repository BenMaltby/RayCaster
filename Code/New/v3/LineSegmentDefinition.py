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
		xps = [self.x1, self.x2, otherLineSeg.x1, otherLineSeg.x2]
		yps = [self.y1, self.y2, otherLineSeg.y1, otherLineSeg.y2]
		xJoined, yJoined = False, False
		newLineSeg = [[None, None], [None, None]]

		if self.orientation == 'H':
			if yps[0] == yps[2]:
				yJoined = True
				newLineSeg[0][1] = yps[0]
				newLineSeg[1][1] = yps[0]

			for i in range(0, 2):
				if len(xps) == 4:
					for j in range(2, 4):
						if len(xps) == 4:
							if xps[i] == xps[j]:
								xJoined = True
								del xps[i]
								del xps[j - 1]
				else:
					break

		elif self.orientation == 'V':
			if xps[0] == xps[2]:
				xJoined = True
				newLineSeg[0][0] = xps[0]
				newLineSeg[1][0] = xps[0]

			for i in range(0, 2):
				if len(yps) == 4:
					for j in range(2, 4):
						if len(yps) == 4:
							if yps[i] == yps[j]:
								yJoined = True
								del yps[i]
								del yps[j - 1]
				else:
					break

		if xJoined and yJoined:
			if self.orientation == 'H':
				newLineSeg[0][0] = xps[0]
				newLineSeg[1][0] = xps[1]

			if self.orientation == 'V':
				newLineSeg[0][1] = yps[0]
				newLineSeg[1][1] = yps[1]

			return lineSeg(newLineSeg[0][0], newLineSeg[0][1], newLineSeg[1][0], newLineSeg[1][1], self.orientation,
						   (randint(0, 254), randint(0, 254), randint(0, 254)))

		return False

	def __repr__(self):
		return f'({self.x1}, {self.y1}) => ({self.x2}, {self.y2})'