from PIL import Image
from Chunk_Struct import ChunkSystem
from VOBJ import createVector

DIMENSIONS = 100
CHUNKSIZE = 10
CSSQUARED = CHUNKSIZE * CHUNKSIZE


class MapTile:
    """stores information about each tile"""
    def __init__(self, x, y, value=2, index=0):
        self.pos = createVector(x, y)
        self.tile = value
        self.index = index

    def __repr__(self):
        return f'{self.tile}'


def coordToIDX(x, y, N=DIMENSIONS):
    return y * N + x


def get_PixelData(image_path):
    image = Image.open(image_path, "r")  # .convert("L")
    pixel_values = list(image.getdata())

    return pixel_values


def GenerateChunks(Data):
    pixelData = get_PixelData(Data)

    chunks = ChunkSystem(1)
    mapList = []
    pCoords = ()
    sprite_coords = []

    for i, cell in enumerate(pixelData):

        x, y = i % DIMENSIONS, i // DIMENSIONS

        idx = coordToIDX(x, y, DIMENSIONS)
        idxInChunk = idx - ((idx // CSSQUARED) * CSSQUARED)

        if sum(pixelData[i]) <= 10:  # wall
            mapList.append(2)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 2, idxInChunk))

        elif sum(pixelData[i]) >= 750:  # floor
            mapList.append(1)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 1, idxInChunk))

        elif pixelData[i] == (0, 255, 0):  # ammo box
            mapList.append(4)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 4, idxInChunk))
            sprite_coords.append(MapTile(x, y, 4))

        elif pixelData[i] == (234, 255, 0):  # spawn point
            mapList.append(5)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 5, idxInChunk))
            sprite_coords.append(MapTile(x, y, 5))
            pCoords = (x, y)

        elif pixelData[i] == (255, 0, 0):  # med kit point
            mapList.append(6)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 6, idxInChunk))
            sprite_coords.append(MapTile(x, y, 6))

        elif pixelData[i] == (170, 0, 255):  # Zombie Basic
            mapList.append(7)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 7, idxInChunk))
            sprite_coords.append(MapTile(x, y, 7))

        elif pixelData[i] == (0, 255, 255):  # torch/flashlight
            mapList.append(10)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 10, idxInChunk))
            sprite_coords.append(MapTile(x, y, 10))

        elif pixelData[i] == (0, 0, 255):  # Star
            mapList.append(11)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 11, idxInChunk))
            sprite_coords.append(MapTile(x, y, 11))

        elif pixelData[i] == (100, 100, 100):  # Machine Gun Pickup
            mapList.append(12)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 12, idxInChunk))
            sprite_coords.append(MapTile(x, y, 12))

        elif pixelData[i] == (255, 100, 0):  # Activate Zombies
            mapList.append(13)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 13, idxInChunk))
            sprite_coords.append(MapTile(x, y, 13))

        elif pixelData[i] == (140, 70, 0):  # Level End Button
            mapList.append(14)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 14, idxInChunk))
            sprite_coords.append(MapTile(x, y, 14))

        elif pixelData[i] == (255, 1, 230):  # Number 1 Button
            mapList.append(16)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 16, idxInChunk))
            sprite_coords.append(MapTile(x, y, 16))

        elif pixelData[i] == (10, 70, 75):  # Gatling gun item
            mapList.append(17)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 17, idxInChunk))
            sprite_coords.append(MapTile(x, y, 17))

        elif pixelData[i] == (0, 96, 64):  # mp5 gun item
            mapList.append(18)
            chunks.insert(MapTile(x // CHUNKSIZE, y // CHUNKSIZE, 18, idxInChunk))
            sprite_coords.append(MapTile(x, y, 18))

        else: raise Exception(f'Unkown tile colour: {pixelData[i]} at coordinate ({x}, {y})')

    return chunks, mapList, pCoords, sprite_coords

# I completely forgot that my map is literally an image, so it is retarded to make a new image...
# def Generate_map_image(img_path, Save_Path: str):
#     im = Image.new("RGB", (DIMENSIONS, DIMENSIONS))
#     pixelData = get_PixelData(img_path)
#     pixels = im.load()
#
#     for i in range(im.size[0]):  # for every pixel:
#         for j in range(im.size[1]):
#
#             idx = coordToIDX(j, i)
#             pixels[j, i] = pixelData[idx]
#
#     im.save(Save_Path)
