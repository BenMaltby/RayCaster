# NOT PART OF FINAL PROJECT, JUST USED FOR TESTING ALGORITHMS

import math
from GenerateChunkMapFromImage import MapTile
from Chunk_Struct import ChunkSystem
from MapProcessing import CELLSIZE
from GenerateChunkMapFromImage import CHUNKSIZE, DIMENSIONS
from TurretDefinition import Turret


LENGTH = math.sqrt(2 * (CHUNKSIZE ** 2))


class Player:
	def __init__(self, x, y, facing, DOV):
		self.pos = (x, y)
		self.facing = facing * (math.pi / 180)
		self.DOV = DOV * (math.pi / 180)


def calc_pCoords(player):
	pCoords = [(int(player.pos[0] // CELLSIZE), int(player.pos[0] // CELLSIZE))]

	for i in range(-2, 3):
		arm = (LENGTH * math.cos(player.facing + (i * player.DOV / 4)) + player.pos[0],
			   LENGTH * math.sin(player.facing + (i * player.DOV / 4)) + player.pos[1])

		cell = (int(arm[0] // CELLSIZE), int(arm[1] // CELLSIZE))

		pCoords.append(cell)

	return pCoords


# None of this works lol, sticking to old chunk frustum
def getAllLineData(edgeChunkSystem: ChunkSystem):
	"""Returns all Map line data in 1 dimensional list"""

	lines = []  # stores all lines in Map

	for y in range(DIMENSIONS//CHUNKSIZE):  # loop over each chunk
		for x in range(DIMENSIONS//CHUNKSIZE):
			chunkEdges = edgeChunkSystem.Query(MapTile(x, y), 0)  # Query system to get line data

			if chunkEdges: lines.extend(chunkEdges[0].edgeData)  # if chunk contains lines than add to line data

	return lines

def cullFrustum(Player: Turret, allLineData: list) -> list:
	"""return list of lines that are within viewing frustum"""

	culledLines = []  # stores all lines within frustum

	# Calculate angle bounds of frustum
	# LFA/RFA = (Left/Right) Frustum Angle
	leftFrustum, rightFrustum = Player.rayData[0], Player.rayData[-1]  # get the first and last ray fired
	LFA, RFA = math.atan2(leftFrustum[1], leftFrustum[0]), math.atan2(rightFrustum[1], rightFrustum[0])  # atan(y/x)

	for idx, line in enumerate(allLineData):  # loop over all lines in map

		p1, p2 = (line.x1, line.y1), (line.x2, line.y2)  # calculate angle to check if between viewing frustum
		p1Angle, p2Angle = math.atan2(p1[1], p1[0]), math.atan2(p2[1], p2[0])

		if LFA < p1Angle < RFA or LFA < p2Angle < RFA:  # if either point between viewing angles then add to culledLines
			culledLines.append(line)

	return culledLines


def main():
	player = Player(45, 45, 0, 180)

	print(calc_pCoords(player))


if __name__ == "__main__":
	main()
