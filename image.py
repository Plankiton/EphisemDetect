from analizer import media
from PIL import Image

def get_normalized(img):
    img_pix_map = img.load()
    for x in range(img.width):
        for y in range(img.height):
            yield x, y, media( img_pix_map[x, y] )
