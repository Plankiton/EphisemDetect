from functools import reduce
from numpy import asarray
from PIL import Image
from sys import argv

def _threshold(img_ar: asarray):
    ar_backup = img_ar
    balance_ar = []
    new_ar = []

    for row in img_ar:
        for pix in row:
            avg = reduce(lambda x, y: (
                x + y
            ), pix[:3])/3
            balance_ar.append(avg)
    balance = reduce(lambda x, y: (
        x + y
    ), balance_ar)/len(balance_ar)

    for x in range(len(ar_backup)):
        row = ar_backup[x]
        new_ar.append([])
        for pix in row:
            avg = reduce(lambda x, y: (
                x + y
            ), pix[:3])/3
            if avg > balance:
                new_ar[x].append(tuple([255 for i in range(3)]))
            else:
                new_ar[x].append(tuple([0 for i in range(3)]))
    return new_ar


def threshold(img: Image):
    if img.mode == 'I':
        img = img.convert('RGBA')
    img_ar = asarray(img)
    new_img = Image.new(mode='RGBA',
                        size = (img.width, img.height))
    pix_map = new_img.load()

    threshold_ar = _threshold(img_ar)
    for x in range(len(img_ar)):
        for y in range(len(img_ar[0])):
            pix_map[x, y] = threshold_ar[x][y]

    return new_img

if '-t' in argv:
    from json import dumps as json
    from os import listdir
    slices = []
    dir_list = listdir('slices')
    data = open('slices.json', 'a')
    data.write('{')
    i = 0
    for slice in dir_list:
        name = slice[:slice.index('_')]
        if '.tiff' in slice and name not in slices:
            slices.append(name)
            print(name)

            top = f'{name}_top.tiff'
            top = asarray(threshold(Image.open(
                f'slices/{top}',
            ))).tolist() if top in dir_list else None

            middle = f'{name}_middle.tiff'
            middle = asarray(threshold(Image.open(
                f'slices/{middle}',
            ))).tolist() if middle in dir_list else None

            bottom = f'{name}_bottom.tiff'
            bottom = asarray(threshold(Image.open(
                f'slices/{bottom}',
            ))).tolist() if bottom in dir_list else None

            dic = {name: {
                'top': top,
                'middle': middle,
                'bottom': bottom
            }}

            data.write(json(dic)+',\n' if i < len(dir_list)-1 \
                       else '\n')

            i += sum([0 if not j else 1 for j in (
                top, middle, bottom
            )])
    data.write('}')
    data.close()
    print('slices threshold saveds')
    exit()

img = Image.open(argv[1])
img = threshold(img)
