from PIL import Image
from Chunk_Struct import ChunkSystem
from VOBJ import createVector

DIMENSIONS = 80
CHUNKSIZE = 10
CSSQUARED = CHUNKSIZE*CHUNKSIZE
MAP_PATH = "GameBoard.png"


class MapTile:
    def __init__(self, x, y, value=2, index=0):
        self.pos = createVector(x, y)
        self.tile = value
        self.index = index

    def __repr__(self):
        return f'{self.tile}'


def coordToIDX(x, y, N = DIMENSIONS):
    return y * N + x


def get_PixelData(image_path):
    image = Image.open(image_path, "r")  # .convert("L")
    pixel_values = list(image.getdata())

    return pixel_values


def GenerateChunks(Data):
    pixelData = get_PixelData(Data)

    chunks = ChunkSystem(CHUNKSIZE)

    for y in range(DIMENSIONS):
        for x in range(DIMENSIONS):

            idx = coordToIDX(x, y, DIMENSIONS)
            idxInChunk = idx - ((idx//CSSQUARED)*CSSQUARED)

            if pixelData[idx] == (0,0,0):
                chunks.insert(MapTile(x, y, 2, idxInChunk))

            elif pixelData[idx] == (255,255,255):
                chunks.insert(MapTile(x, y, 1, idxInChunk))

    return chunks
