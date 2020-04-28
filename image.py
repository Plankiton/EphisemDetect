from PIL import Image, PyAccess

def get_gray_shade(img):
    img = img.convert(mode='I', matrix=None, dither=None, palette=0, colors=256)
    img_pix_map = img.load()
    for x in range(img.width):
        for y in range(img.height):
            pixel = img_pix_map[x, y]
            yield x, y, pixel

def get_pix_map(pix_map):
    for x in range(len(pix_map)):
        for y in range(len(pix_map[0])):
            yield x, y, pix_map[x][y]
