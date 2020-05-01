from json import loads as json
from sys import argv as arg
from analizer import *
from image import *

data = json(open('./local_binary_patt.json').read())

img_path = arg[1]
img = Image.open(img_path)
try:
    img_type = img_path[img_path.index('_')+1:img_path.rindex('.tiff')]
except:
    img_type = None
pix_map = None


if 'rgb' in img.mode.strip():
    pix_map = get_lbp(img, pix_map = get_gray_shade(img))
else:
    pix_map = get_lbp(img)

percentage = 0
for lbp in data:
    if img_type:
        for cat_perc in compare(data[lbp][img_type], pix_map):
            percentage += cat_perc
    else:
        for cat in data[lbp]:
            for cat_perc in compare(data[lbp][cat], pix_map):
                percentage += cat_perc
percentage /= len(data)

print(percentage)
