from MapProcessing import Map, CELLSIZE
from random import randint
from LineSegmentDefinition import lineSeg


def primitiveEdges() -> list:  # First calculate each cell edges
	sizeOfMap = len(Map[0])

	WallList = []

	for y, row in enumerate(Map):
		for x, col in enumerate(row):

			if Map[y][x] == 2:  # Only outline wall cells
				gridCell = [x * CELLSIZE, y * CELLSIZE]

				# Check above
				if y != 0:
					if Map[y - 1][x] != 2:  # if we are not on the top row, we can index above
						WallList.append(lineSeg(gridCell[0], gridCell[1], gridCell[0] + CELLSIZE, gridCell[1], 'H', (randint(0, 254), randint(0, 254), randint(0, 254))))

				# Check right
				if x != sizeOfMap-1:
					if Map[y][x + 1] != 2:  # if we are not on the right edge, we can index to the right
						WallList.append(lineSeg(gridCell[0] + CELLSIZE, gridCell[1], gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254))))

				# Check below
				if y != sizeOfMap-1:
					if Map[y + 1][x] != 2:  # if we are not on the bottom edge, we can index below
						WallList.append(lineSeg(gridCell[0], gridCell[1] + CELLSIZE, gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'H', (randint(0, 254), randint(0, 254), randint(0, 254))))

				# Check left
				if x != 0:
					if Map[y][x-1] != 2:  # if we are not on the left edge, we can index to the left
						WallList.append(lineSeg(gridCell[0], gridCell[1], gridCell[0], gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254))))

	return WallList


def calculatedEdges(edgeList) -> list:

	for idx in range(len(edgeList)):
		if idx < len(edgeList):
			startingLineSeg = edgeList[idx]
		else:
			break

		stVertical = False if startingLineSeg.y2 - startingLineSeg.y1 == 0 else True
		stHorizontal = True if not stVertical else False

		jdx = 0

		while jdx < len(edgeList):
			addingLineSeg = edgeList[jdx]

			if startingLineSeg is not addingLineSeg:
				adVertical = False if addingLineSeg.y2 - addingLineSeg.y1 == 0 else True
				adHorizontal = True if not adVertical else False

				if stVertical and adVertical or stHorizontal and adHorizontal:
					newLineSeg = startingLineSeg.isSharedPoint(addingLineSeg)

					if newLineSeg:
						startingLineSeg = newLineSeg
						edgeList[idx] = newLineSeg
						del edgeList[jdx]

					else:
						jdx += 1
				else:
					jdx += 1

			else:
				jdx += 1

	return edgeList
