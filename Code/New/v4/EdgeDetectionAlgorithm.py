from MapProcessing import CELLSIZE
from random import randint
from LineSegmentDefinition import lineSeg
from Chunk_Struct import ChunkSystem
from GenerateChunkMapFromImage import MapTile, CHUNKSIZE, DIMENSIONS
from VOBJ import createVector


class edgeChunk:
	def __init__(self, x, y, edgeData=0):
		self.pos = createVector(x, y)
		self.edgeData = edgeData

	def __repr__(self):
		return f'{self.edgeData}'


def primitiveEdges(GridChunkMap: ChunkSystem) -> ChunkSystem:  # First calculate each cell edges

	primEdgeSystem = ChunkSystem(1)

	for i in range(DIMENSIONS//CHUNKSIZE):
		for j in range(DIMENSIONS//CHUNKSIZE):
			chunk = GridChunkMap.Query(MapTile(j, i), 0)
			for z, cell in enumerate(chunk):

				if cell.tile == 2:  # Only outline wall cells
					x = z % CHUNKSIZE
					y = z // CHUNKSIZE
					gridCell = [(x + j * CHUNKSIZE) * CELLSIZE, (y + i * CHUNKSIZE) * CELLSIZE]

					# Check above
					if z > CHUNKSIZE - 1:
						if chunk[z - CHUNKSIZE].tile != 2:  # if we are not on the top row, we can index above
							primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1], gridCell[0] + CELLSIZE, gridCell[1], 'H', (randint(0, 254), randint(0, 254), randint(0, 254)))))
					# else:
					# 	primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1], gridCell[0] + CELLSIZE, gridCell[1], 'H', (randint(0, 254), randint(0, 254), randint(0, 254)))))

					# Check right
					if (z - (CHUNKSIZE-1)) % CHUNKSIZE != 0:
						if chunk[z + 1].tile != 2:  # if we are not on the right edge, we can index to the right
							primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0] + CELLSIZE, gridCell[1], gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254)))))
					# else:
					# 	primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0] + CELLSIZE, gridCell[1], gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254)))))

					# Check below
					if z < len(chunk) - CHUNKSIZE:
						if chunk[z + CHUNKSIZE].tile != 2:  # if we are not on the bottom edge, we can index below
							primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1] + CELLSIZE, gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'H', (randint(0, 254), randint(0, 254), randint(0, 254)))))
					# else:
					# 	primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1] + CELLSIZE, gridCell[0] + CELLSIZE, gridCell[1] + CELLSIZE, 'H', (randint(0, 254), randint(0, 254), randint(0, 254)))))

					# Check left
					if z % CHUNKSIZE != 0:
						if chunk[z - 1].tile != 2:  # if we are not on the left edge, we can index to the left
							primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1], gridCell[0], gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254)))))
					# else:
					# 	primEdgeSystem.insert(edgeChunk(j, i, lineSeg(gridCell[0], gridCell[1], gridCell[0], gridCell[1] + CELLSIZE, 'V', (randint(0, 254), randint(0, 254), randint(0, 254)))))

	return primEdgeSystem


def calculatedEdges(primEdgeSystem: ChunkSystem) -> ChunkSystem:

	edgeSystem = ChunkSystem(1)

	for i in range(DIMENSIONS//CHUNKSIZE):
		for j in range(DIMENSIONS//CHUNKSIZE):
			edgeList = []
			edgeChunkList = primEdgeSystem.Query(MapTile(j, i), 0)
			# del edgeChunkList[::2]

			for tidx, temp in enumerate(edgeChunkList):
				edgeList.append(temp.edgeData)

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

			if edgeList: edgeSystem.insert(edgeChunk(j, i, edgeList))

	return edgeSystem
