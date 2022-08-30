from PIL import Image
from random import randint

def get_PixelData(image_path):
    image = Image.open(image_path, "r")  # .convert("L")
    pixel_values = list(image.getdata())

    return pixel_values

def main():
    im = Image.new("RGB", (100,100))
    pixels = im.load()

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = (randint(0, 255), randint(0, 255), randint(0, 255))

    im.save("test_images/img1.png")

if __name__ == "__main__":
    main()