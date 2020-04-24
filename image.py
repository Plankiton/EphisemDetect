from PIL import Image

def get_color_matrix(img):
    for x in range(img.width):
        for y in range(img.height):
            yield x, y, img.getpixel( (x, y) )
