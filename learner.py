from sys import argv as args
from os import listdir
from analizer import *
from image import *
from json import dumps

imgs = [f'slices/{i}' for i in listdir('slices')]
lbps = {}

for img in imgs:
    img_name = img[:img.index('_')]
    img_type = img[img.index('_')+1:img.rindex('.tiff')]
    print(img,'\n',img_name,'\n',img_type,'\n')
    if img_name not in lbps:
        lbps[img_name] = dict(top = None, middle = None, bottom = None)

    img = Image.open(img)
    img_pix_map = img.load()

    pix_map = [[None for j in range(img.height)]
                   for i in range(img.width)]
    for x in range(img.height):
        for y in range(img.width):
            pix_map[x][y] = img_pix_map[x, y]

    lbps[img_name][img_type] = do_lbp_on_pix_map(pix_map)

open('local_binary_patt.json').write(dumps(lbps))
