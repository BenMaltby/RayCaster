# VERY OLD RAY CAST CONCEPT FUNCTION
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



# RAY CAST VERTICAL FAIL
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



# INITIAL APPROACH TO EDGE CALCULATIONS
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




# LENGTH = CHUNKWIDTH  # math.sqrt(2 * (CHUNKWIDTH ** 2))
# LENGTH2 = math.sqrt(2 * (CHUNKWIDTH ** 2))
# def calc_pCoords(player):
# 	pCoords = [(int(player.pos.x // CHUNKWIDTH), int(player.pos.y // CHUNKWIDTH))]
# 	lengths = [LENGTH, LENGTH2, LENGTH, LENGTH2, LENGTH]
#
# 	for i in range(-2, 3):
# 		arm = (lengths[i+2] * math.cos(player.facing + (i * (player.angleOfVision*RADIAN) / 4)) + player.pos.x,
# 			   lengths[i+2] * math.sin(player.facing + (i * (player.angleOfVision*RADIAN) / 4)) + player.pos.y)
#
# 		cell = (int(arm[0] // CHUNKWIDTH), int(arm[1] // CHUNKWIDTH))
#
# 		pCoords.append(cell)
#
# 	return pCoords




# print(intersectionX, intersectionY, int(coordToIDX(intersectionX//CELLSIZE, intersectionY//CELLSIZE)))
# cellType = MapAsCells[int(coordToIDX(intersectionX//CELLSIZE, intersectionY//CELLSIZE))]
# if cellType == 1:  # if tile is a floor tile
# 	newCoords = calculate_Nearest_Cell(intersectionX, intersectionY)
# 	cellType = MapAsCells[int(coordToIDX(newCoords[0] // CELLSIZE, newCoords[1] // CELLSIZE))]



# SPRITE RENDERING FAILS (MANY DAYS OF RESEARCH)

# h.x = entity.x - player.x
# h.y = entity.y - player.y
#
# p = atan2(-h.y / h.x) * (180 / PI)
#
# if p > 360:
# 	p -= 360
# if p < 0:
# 	p += 360
#
# q = player_rot + (fov / 2) - p
#
# if player_rot in quadrant 1 and p in quadrant 4:
# 	q += 360
# if player_rot in quadrant 4 and p in quadrant 1:
# 	q -= 360
#
# sprite_screen.x = q * (projection_plane_width / fov)
# sprite_screen.y = 100(projection_plane_height / 2 = 200 / 2 = 100)


# vx, vy = entity.x - player.pos.x, entity.y - player.pos.y
# theta = (3*math.pi)/2 - player.facing
# nx, ny = rotate((vx, vy), theta) # vx * math.cos(theta) + vy * math.sin(theta), vx * (-math.sin(theta)) + vy * math.cos(theta)
# distance = math.sqrt(vx**2 + vy**2)
# height = (CELLSIZE*200) / distance if distance > 0 else 1200  # calculate how tall the wall column should be
# eX = nx * distance/vy
# pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(eX, 400, height, height))

# FOVO2 = (player.angleOfVision * RADIAN) / 2
# vx, vy = entity.x - player.pos.x, entity.y - player.pos.y
# theta = math.atan2(vy, vx) + math.pi
# # print(player.facing - FOVO2, player.facing, player.facing + FOVO2, theta)
# # exit()
# if player.facing - FOVO2 < theta < player.facing + FOVO2:
# 	x = ((player.facing - theta) / FOVO2) * WIDTH
# else:
# 	x = -100
# pygame.draw.rect(screen, (0,255,0), pygame.Rect(x, 400, 100, 100))

# I cannot get sprite rendering to work

# xInc = entity.x - player.pos.x
# yInc = entity.y - player.pos.y
# FOV = player.angleOfVision
#
# thetaTemp = math.atan2(yInc, xInc)
# thetaTemp /= RADIAN
# thetaTemp %= 360
#
# yTmp = player.facing + FOV/2 - thetaTemp
# if thetaTemp > 270 and thetaTemp < 90: yTmp = player.facing + FOV/2 - thetaTemp + 360
# if player.facing > 270 and thetaTemp < 90: yTmp = player.facing + FOV/2 - thetaTemp - 360
#
# xTmp = yTmp * WIDTH / FOV
#
# pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(xTmp, 400, 10, 10))

# sx, sy, sz = entity.x - player.pos.x, entity.y - player.pos.y, entity.z
# CS, SN = math.cos(player.facing), math.sin(player.facing)
# a = sy * CS + sx * SN
# b = sx * CS - sy * SN
# sx, sy = a, b
#
# sx = (sx * 108/sy)+(WIDTH/2)
# sy = (sz * 108/sy)+(HEIGHT/2)
#
# pygame.draw.rect(screen, (0,0,255), pygame.Rect(sx, sy, 10, 10))

# vx, vy = entity.x - player.pos.x, entity.y - player.pos.y
# distance = math.sqrt(vx**2 + vy**2)
# height = (CELLSIZE*200) / distance if distance > 0 else 1200  # calculate how tall the wall column should be
# FOVO2 = player.angleOfVision / 2
# x = ((math.atan2(entity.x, entity.y) - player.facing) / RADIAN) % 360  # FOVO2 - (math.atan2(vy, vx) - player.facing)
# pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x * (columnWidth), HEIGHT/2 - height/2, height, height))


# planeX, planeY = r * math.cos(player.facing + FOVO2), r * math.sin(player.facing + FOVO2)
# # planeX, planeY = r * math.cos(player.facing), r * math.sin(player.facing)
# dirX, dirY = args[0] * math.cos(player.facing), args[0] * math.sin(player.facing)

# lp = createVector(r * math.cos(player.facing - FOVO2), r * math.sin(player.facing - FOVO2))
# rp = createVector(r * math.cos(player.facing + FOVO2), r * math.sin(player.facing + FOVO2))
# planeX, planeY = (rp.x - lp.x, rp.y - lp.y)





# Old Cluncky is shared point
# def isSharedPoint(self, otherLineSeg):
# 	xps = [self.x1, self.x2, otherLineSeg.x1, otherLineSeg.x2]
# 	yps = [self.y1, self.y2, otherLineSeg.y1, otherLineSeg.y2]
# 	xJoined, yJoined = False, False
# 	newLineSeg = [[None, None], [None, None]]
#
# 	if self.orientation == 'H':
# 		if yps[0] == yps[2]:
# 			yJoined = True
# 			newLineSeg[0][1] = yps[0]
# 			newLineSeg[1][1] = yps[0]
#
# 		for i in range(0, 2):
# 			if len(xps) == 4:
# 				for j in range(2, 4):
# 					if len(xps) == 4:
# 						if xps[i] == xps[j]:
# 							xJoined = True
# 							del xps[i]
# 							del xps[j - 1]
# 			else:
# 				break
#
# 	elif self.orientation == 'V':
# 		if xps[0] == xps[2]:
# 			xJoined = True
# 			newLineSeg[0][0] = xps[0]
# 			newLineSeg[1][0] = xps[0]
#
# 		for i in range(0, 2):
# 			if len(yps) == 4:
# 				for j in range(2, 4):
# 					if len(yps) == 4:
# 						if yps[i] == yps[j]:
# 							yJoined = True
# 							del yps[i]
# 							del yps[j - 1]
# 			else:
# 				break
#
# 	if xJoined and yJoined:
# 		if self.orientation == 'H':
# 			newLineSeg[0][0] = xps[0]
# 			newLineSeg[1][0] = xps[1]
#
# 		if self.orientation == 'V':
# 			newLineSeg[0][1] = yps[0]
# 			newLineSeg[1][1] = yps[1]
#
# 		return lineSeg(newLineSeg[0][0], newLineSeg[0][1], newLineSeg[1][0], newLineSeg[1][1], self.orientation,
# 					   (randint(0, 254), randint(0, 254), randint(0, 254)))
#
# 	return False




# vCurrentCell = createVector(math.floor(Player.pos.x), math.floor(Player.pos.y))
# vTargetCell = newPosition
# vAreaTL = createVector(VOBJ.min(vTargetCell.x, vCurrentCell.x), VOBJ.min(vTargetCell.y, vCurrentCell.y))
# vAreaTL.sub(createVector(MapProcessing.CELLSIZE, MapProcessing.CELLSIZE))
# vAreaTL.x, vAreaTL.y = VOBJ.max(0, vAreaTL.x), VOBJ.max(0, vAreaTL.y)
# vAreaBR = createVector(VOBJ.max(vTargetCell.x, vCurrentCell.x), VOBJ.max(vTargetCell.y, vCurrentCell.y))
# vAreaBR.add(createVector(MapProcessing.CELLSIZE, MapProcessing.CELLSIZE))
# vAreaBR.x, vAreaBR.y = VOBJ.min(HEIGHT, vAreaBR.x), VOBJ.min(HEIGHT, vAreaBR.y)
#
# print(vAreaTL, vAreaBR)
#
# for y in range(vAreaTL.y, vAreaBR.y):
# 	for x in range(vAreaTL.x, vAreaBR.y):
# 		if Map[int(coordToIDX(x, y))] == 2:
# 			cell = createVector(x * MapProcessing.CELLSIZE, y * MapProcessing.CELLSIZE)
# 			vNearestPoint = createVector(VOBJ.max(cell.x, VOBJ.min(newPosition.x, cell.x + 1)), VOBJ.max(cell.y, VOBJ.min(newPosition.y, cell.y + 1)))
# 			vRayToNearest = VOBJ.sub2Vec(vNearestPoint, newPosition)
# 			overlap = 8 - vRayToNearest.mag()
#
# 			if overlap > 0 and vRayToNearest.mag() != 0:
# 				vRayToNearest.normalize()
# 				vRayToNearest.mult(overlap)
# 				newPosition.sub(vRayToNearest)

# for y in range(Player.MapCell[1] - 1, Player.MapCell[1] + 1):
# 	for x in range(Player.MapCell[0] - 1, Player.MapCell[0] + 1):
#
# 		if Map[int(coordToIDX(x, y))] == 2:
# 			cell = createVector(x * MapProcessing.CELLSIZE, y * MapProcessing.CELLSIZE)
# 			# vNearestPoint = createVector(VOBJ.max(cell.x, VOBJ.min(newPosition.x, cell.x + 1)), VOBJ.max(cell.y, VOBJ.min(newPosition.y, cell.y + 1)))
# 			# vRayToNearest = VOBJ.sub2Vec(vNearestPoint, newPosition)
# 			# overlap = 8 - vRayToNearest.mag()
# 			#
# 			# if overlap > 0 and vRayToNearest.mag() != 0:
# 			# 	vRayToNearest.normalize()
# 			# 	vRayToNearest.mult(overlap)
# 			# 	newPosition.sub(vRayToNearest)
#
# 			clampedPoint = createVector(VOBJ.clamp(cell.x, cell.x + 1, newPosition.x), VOBJ.clamp(cell.y, cell.y + 1, newPosition.y))
# 			distanceVec = VOBJ.sub2Vec(clampedPoint, newPosition)
# 			overlap = MapProcessing.CELLSIZE - distanceVec.mag()
#
# 			if overlap > 0 and distanceVec.mag() != 0:
# 				distanceVec.normalize()
# 				distanceVec.mult(-overlap)
# 				newPosition.add(distanceVec)



# old player movement code
# if keys[pygame.K_a]:  # a = STRAFE LEFT
# 	# Player.Move_LEFT()
# 	# if Player.Check_Collision(Map, sp):
# 	# 	Player.Move_RIGHT()
# 	Player.vel.add(createVector(math.cos(Player.facing - math.pi / 2), math.sin(Player.facing - math.pi / 2)))
#
# if keys[pygame.K_d]:  # d = STRAFE RIGHT
# 	# Player.Move_RIGHT()
# 	# if Player.Check_Collision(Map, sp):
# 	# 	Player.Move_LEFT()
# 	Player.vel.add(createVector(math.cos(Player.facing + math.pi / 2), math.sin(Player.facing + math.pi / 2)))
#
# if keys[pygame.K_w]:  # w = FORWARD
# 	# Player.Move_UP()
# 	# if Player.Check_Collision(Map, sp):
# 	# 	Player.Move_DOWN()
# 	Player.vel.add(createVector(math.cos(Player.facing), math.sin(Player.facing)))
#
# if keys[pygame.K_s]:  # s = BACKWARDS
# 	# Player.Move_DOWN()
# 	# if Player.Check_Collision(Map, sp):
# 	# 	Player.Move_UP()
# 	Player.vel.add(createVector(math.cos(Player.facing - math.pi), math.sin(Player.facing - math.pi)))



# Old mini map screen
# def MiniMap2D(screen, mmWidth, Player, offset, MapChunks):
#     mmCellSize = mmWidth / DIMENSIONS
#
#     for i in range(DIMENSIONS*DIMENSIONS):
#         x = i % DIMENSIONS
#         y = i // DIMENSIONS
#         pos = createVector(x * mmCellSize, y * mmCellSize)
#         PlayerChunkData = MapChunks.Query(MapTile(x, y), 0)
#         PlayerCellIndex = (y // (DIMENSIONS / CHUNKSIZE)) * CHUNKSIZE + (
#                     x // (DIMENSIONS / CHUNKSIZE))
#         col = PlayerChunkData[int(PlayerCellIndex)].tile
#         pygame.draw.rect(screen, MapMaterials[col].colour,
#                          pygame.Rect(pos.x + offset[0], pos.y + offset[1], mmCellSize, mmCellSize))
#
#     px, py = (Player.pos.x/HEIGHT)*mmWidth + offset[0], (Player.pos.y/HEIGHT)*mmWidth + offset[1]
#     pygame.draw.line(screen, (255, 0, 0), (px, py), (mmWidth*0.05*math.cos(Player.facing)+px, mmWidth*0.05*math.sin(Player.facing)+py))
#     pygame.draw.circle(screen, (0, 255, 0), (px, py), mmWidth*0.01)



# Acid Trip Wall Code
# if player.on_acid > -1: Acid_trip_column_width = abs(math.sin(args[3] + (math.pi / 2 * int(idx / 2))))
# if player.on_acid > -1:
# 	pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, (HEIGHT/2 - Acid_trip_column_width * columnHeight/2), Acid_trip_column_width * 2 * columnWidth + columnWidth,
# 											  Acid_trip_column_width * columnHeight))

# if not player.on_acid > -1:
# if player.on_acid > -1:
# 	pygame.draw.rect(screen, col, pygame.Rect(idx * columnWidth, (HEIGHT/2 - Acid_trip_column_width * columnHeight/2), Acid_trip_column_width * 2 * columnWidth + columnWidth,
# 											  Acid_trip_column_width * columnHeight))
# if not player.on_acid > -1:






# ENEMIE WAITING SO THEY DON'T BUNCH UP

# # used to delay enemy waiting so enemies don't overlap
# if pygame.time.get_ticks() == self.waitUntil: self.isWaiting = False

# if not self.isWaiting:
# 	for idx, zombie in enumerate(z_system):
# 		if zombie is not self and len(z_system[idx].targets) > 1:
# 			if z_system[idx].targets[1] == self.targets[0]:  # if zombie in way
# 				print(idx)
# 				self.isWaiting = True
# 				self.waitUntil = pygame.time.get_ticks() + 50 * idx  # 50 milliseconds





# Old gunshot timing

# if 1 < gunshot_timer < Player.weapon.fire_rate and Player.ammo_count > 0:
# 	Player.shooting = True  # used to show shooting gun image
# 	if not shot_fired and gunshot_timer == 2:  # fire shot
# 		Player.ammo_count -= 1
# 		shot_fired = True
# 		cast_zombie(z_system, Player)  # handle detecting zombie hits and deal damage

# elif gunshot_timer > Player.weapon.fire_rate:
# 	gunshot_timer = -Player.weapon.fire_rate
# 	Player.shooting = False
# 	shot_fired = False
# gunshot_timer += 1

# elif not mouseDown:

#     gunshot_timer = 0
#     shot_fired = False







# OLD GUI SETTINGS CODE

# GUI BOILERPLATE CODE
# View Mode Button Instances
# RayCastViewButton = GEWY.Button(5, 10, 20, 20, "3D View", True)
# BirdsEyeViewButton = GEWY.Button(5, 40, 20, 20, "2D View", True)
# RenderWallLinesButton = GEWY.Button(5, 70, 20, 20, "2D WireFrame", True)
# RenderMapImageButton = GEWY.Button(5, 100, 20, 20, "2D Map Image", True)
# ViewButtonWrapper = GEWY.Wrapper(10, 35, 200, 100, [RayCastViewButton, BirdsEyeViewButton, RenderWallLinesButton, RenderMapImageButton], "Change View")
# GEWY.GUI_OBJECTS.append(ViewButtonWrapper)

# brightnessSettings = False  # True when debugging
# # Brightness Setting slider instances
# sceneBrightnessSlider = GEWY.VariableSlider(5, 30, 100, 0, 1, "Scene", True, 1)
# wallBrightnessSlider = GEWY.VariableSlider(5, 70, 100, 0, 2, "Walls", True, 2)
# flashBrightnessSlider = GEWY.VariableSlider(5, 110, 100, 3, 15, "Gun Flash", True, 3)
# BrightnessSlidersWrapper = GEWY.Wrapper(170, 35, 150, 130, [sceneBrightnessSlider, wallBrightnessSlider, flashBrightnessSlider], "Brightness Options")
# GEWY.GUI_OBJECTS.append(BrightnessSlidersWrapper)

# resumeButton = GEWY.Button((WIDTH / 2) - 100, HEIGHT / 2, 200, 40, "Resume", False, (-135, -8))
# pauseMenuWrapper = GEWY.Wrapper(0, 0, WIDTH, HEIGHT, [resumeButton], "Pause Menu")
# GEWY.GUI_OBJECTS.append(pauseMenuWrapper)

# # GUI Tab system setup
# mainTabs = GEWY.TabSystem()
# mainTabs.addTab(ViewButtonWrapper)
# if brightnessSettings: mainTabs.addTab(BrightnessSlidersWrapper)
# GEWY.GUI_OBJECTS.append(mainTabs)





# First state of pause screen
# # Pause screen code
# if game_paused and Player.health > 0:
# 	Tabs.disableAllTabs()
# 	Resume_Wrapper.isOpen, Restart_Wrapper.isOpen, Exit_Wrapper.isOpen = True, True, True
# 	Restart_Wrapper.wrapperPos.y, Exit_Wrapper.wrapperPos.y = 410, 520
# 	Restart_Wrapper.top_bar_drag()
# 	Exit_Wrapper.top_bar_drag()

# 	pause_screen.fill((50, 50, 50))
# 	textsurface = pauseMenuText.render(f'PAUSED', False, (255, 255, 255))  # renders onto screen
# 	pause_screen.blit(textsurface, ((WIDTH / 2) - 140, 30))	
# 	screen.blit(pause_screen, (0, 0))
# 	GEWY.display(screen)

# 	if Resume_Button.returnState(): 
# 		game_paused = False
# 		Player.canMove = True
# 		pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
# 		Resume_Button.state = False

# 	if Restart_Button.returnState(): 
# 		pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
# 		Restart_Button.state = False
# 		return "run"

# 	if Exit_Button.returnState(): return "end"






# First state of death screen
# Player.canMove = False

# Tabs.disableAllTabs()
# Restart_Wrapper.isOpen, Exit_Wrapper.isOpen = True, True
# Restart_Wrapper.wrapperPos.y, Exit_Wrapper.wrapperPos.y = 300, 460
# Restart_Wrapper.top_bar_drag()
# Exit_Wrapper.top_bar_drag()

# pause_screen.fill((255, 0, 0))
# textsurface = pauseMenuText.render(f'DEAD', False, (255, 255, 255))  # renders onto screen
# pause_screen.blit(textsurface, ((WIDTH / 2) - 100, 30))	
# screen.blit(pause_screen, (0, 0))
# GEWY.display(screen)

# if Restart_Button.returnState(): 
# 	pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
# 	Restart_Button.state = False
# 	return "run"

# if Exit_Button.returnState(): return "end"







# def GameState4():  # Death screen
# 	return_command = "gm1"

# 	Tabs.disableAllTabs()
# 	Restart_Wrapper.isOpen, Exit_Wrapper.isOpen = True, True
# 	pygame.mouse.set_visible(False)

# 	# Game loop
# 	running = True
# 	while running:

# 		# 1 Process input/events
# 		clock.tick(FPS)  # will make the loop run at the same speed all the time
# 		for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
# 			# listening for the X button at the top
# 			if event.type == pygame.QUIT:
# 				running = False

# 			# Handles all input for my GUI
# 			mVec = pygame.mouse.get_pos()
# 			GEWY.handleEvents(event, mVec, screen)

# 		if Restart_Button.returnState(): return return_command

# 		if Exit_Button.returnState(): return "end"

# 		# 3 Draw/render
# 		screen.fill(BLACK)
# 		GEWY.display(screen)  # handles rendering of GEWY objects

# 		textsurface = pauseMenuText.render(f'DEAD', False, (255, 255, 255))  # renders onto screen
# 		screen.blit(textsurface, ((WIDTH / 2) - 180, 30))

# 		pygame.display.flip()  # Done after drawing everything to the screen

# 	return return_command

# if CurrentGameState == 4:
# 	command = GameState4()