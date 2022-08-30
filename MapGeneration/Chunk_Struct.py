class PointOBJ:
    """Definition of point to simulate vector"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class ChunkSystem:
    def __init__(self, cellSize):
        # Map to store grid cells
        self.chunkMap = {}

        # width and height of each cell in pixels
        self.cellSize = cellSize

    def __repr__(self):
        return f'{self.chunkMap}'

    # Method to insert into chunk system
    def insert(self, point):

        # Create grid PointOBJ
        currChunk = PointOBJ(point.pos.x // self.cellSize, point.pos.y // self.cellSize)

        # Make unique chunkKey for grid coordinate
        chunkKey = f'{currChunk.x} {currChunk.y}'

        # If chunk Map does not yet contain points at chunk index
        if chunkKey not in self.chunkMap:
            # Create array of Boid objects at chunk coordinate
            self.chunkMap.update({chunkKey: [point]})

        # If chunk Map already contains points at chunk index
        else:
            # add point to corresponding point array at chunk coordinate
            self.chunkMap[chunkKey].append(point)

    # Method to find all points within a given radius of "Query Point"
    def Query(self, point, radius):

        # array containing all points within the radius
        adjacentBoids = []

        # Create grid PointOBJ
        currChunk = PointOBJ(point.pos.x // self.cellSize, point.pos.y // self.cellSize)

        for y in range(int(currChunk.y) - radius, int(currChunk.y) + radius + 1):
            for x in range(int(currChunk.x) - radius, int(currChunk.x) + radius + 1):

                # Make unique chunk Key for grid coordinate
                chunkKey = f'{x} {y}'

                # if there are boids in the chunk,
                # and we aren't looking at our own chunk
                if chunkKey in self.chunkMap:
                    # add all boids to final array
                    adjacentBoids += self.chunkMap[chunkKey]

        return adjacentBoids

    def gCell(self, point):
        return PointOBJ((point.pos.x // self.cellSize)*self.cellSize, (point.pos.y // self.cellSize)*self.cellSize)