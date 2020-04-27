from PIL import Image, PyAccess
from analizer import media

def get_gray_shade(img, mode = 'rgb'):
    modes = dict(
        rgb = media,
        gray_shade = int
    )

    img_pix_map = img.load()
    print(img_pix_map[0,0])
    for x in range(img.width):
        for y in range(img.height):
            yield x, y, modes[mode]( img_pix_map[x, y] )


def get_pix_map(pix_map):
    for x in range(len(pix_map)):
        for y in range(len(pix_map[0])):
            yield x, y, tuple([int(pix_map[x][y]) for i in range(3)])
