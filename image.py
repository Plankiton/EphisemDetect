from PIL import Image, PyAccess
from analizer import media

def get_gray_shade(img):
    img_pix_map = img.load()
    for x in range(img.width):
        for y in range(img.height):
            yield x, y, media( img_pix_map[x, y] )


def get_pix_map(new_pix_map):
    for x in range(len(new_pix_map)):
        for y in range(len(new_pix_map[0])):
            yield x, y, tuple([new_pix_map[x][y] for i in range(3)])
