# def CastRay(sPos: createVector, angle: float):
#     global RayCol
#
#     CellSize = MapProcessing.CELLSIZE
#     gCell = createVector(sPos.x // CellSize, sPos.y // CellSize)
#     hitWall = False
#     xStep, yStep = 0, 0
#     rayGridCell = createVector()
#
#     for i in range(10):
#         xComp = ((gCell.x + 1) * CellSize - sPos.x) + (CellSize * xStep)
#         #yComp = ((gCell.y + 1) * CellSize - sPos.y) + (CellSize * yStep)
#         yCell = (math.tan(angle) * xComp) // CellSize
#         xStep += 1
#
#         rayGridCell.x = gCell.x + (xComp // CellSize)
#         #rayGridCell.y = gCell.y + (yComp // CellSize)
#         if rayGridCell.x < len(MapProcessing.Map[0]) and rayGridCell.x >= 0:
#             if yCell < len(MapProcessing.Map) and yCell >= 0:
#                 if MapProcessing.Map[int(yCell)][int(rayGridCell.x)] == 2:
#                     hitWall = True
#                     RayCol = (255, 0, 0)
#                     return
#     RayCol = (0, 255, 0)
#
#         # gCell.x + (xDist // cellsize)




# def castVertical(distToNextCell, ):
#
#
#
# def RayCast():
#     viewLength = 20  # tiles
#     viewingDistance = 0
#
#     while viewingDistance < viewLength:
#         """
#         cast horizontal ray then
#         if it hits a wall we can stop and know its a horizontal hit
#
#         then do the same for vertical
#
#         then if no hit, increase viewingDistance
#         """




# def calculatedEdges(edgeList) -> list:
#
# 	# NewEdgeList = []
# 	swap = False
#
# 	for idx, startingEdge in enumerate(edgeList):
# 		delCounter = 0
# 		stVertical = False if startingEdge.y2 - startingEdge.y1 == 0 else True
# 		stHorizontal = True if not stVertical else False
#
# 		for jdx, addedEdge in enumerate(edgeList):
# 			if swap:
# 				jdx -= 1 * delCounter
# 				addedEdge = edgeList[jdx]
# 			if startingEdge is not addedEdge:  # if they are not the same edge
#
# 				adVertical = False if addedEdge.y2 - addedEdge.y1 == 0 else True
# 				adHorizontal = True if not adVertical else False
#
# 				if stVertical and adVertical or stHorizontal and adHorizontal:  # if they're in the same direction
# 					newLineSeg = startingEdge.isSharedPoint(addedEdge)
# 					#print(newLineSeg)
#
# 					if newLineSeg:
# 						startingEdge = newLineSeg
# 						edgeList[idx] = newLineSeg
# 						del edgeList[jdx]
# 						swap = True
# 						delCounter += 1
# 					else:
# 						swap = False
#
#
# 	return edgeList