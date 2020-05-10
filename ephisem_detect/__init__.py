#!/usr/bin/python3

from functools import reduce
from numpy import asarray
from PIL import Image
from sys import argv

def compress_map(img_map:list) -> list:
    '''
    Compress the image pix map
    returns a compressed pix map
    '''

    c = 0
    new_map = []
    w, h = len(img_map), len(img_map[0])
    size_range = int((w + h) / 2 * 0.006)
    for x in range(0, w, size_range):
        new_map.append([])
        for y in range(0, w, size_range):
            xend = x+size_range
            xend = xend if xend < w else w
            yend = y+size_range
            yend = yend if yend < w else w

            pix_range = [[
                img_map[i][j] for j in range(y, yend)
            ] for i in range(x, xend)]

            n = 0
            for i in pix_range:
                for j in i:
                    n += 1 if j == (0,0,0) else 0
            pixel = n*100/len(i) > 50
            new_map[c].append(pixel)
        c += 1
    return new_map

def prepar_data(type_slice:str = 'middle'):
    '''
    Load and compress all slices on ./slices folder
    returns a list with all slices loaded
    '''

    from os import listdir

    slices = {}
    dir_list = listdir('slices')
    for i in dir_list:
        if type_slice not in i:
            dir_list.remove(i)

    for slice in dir_list:
        name = slice[:slice.index('_')]
        print(f'  -> {name}')
        if '.tiff' in slice and name not in slices:

            for t in ['top', 'bottom', 'middle']:
                t = f'{name}_{t}.tiff'
                d = f'slices/{t}'
                t = compress_map(threshold(Image.open(
                    d,
                ))) if t in dir_list else None

                slices[name] = {
                    'data': t,
                    'dir': d
                }
    return slices

def _threshold(img_ar: asarray):
    '''
    returns a array only with black or white pixels
    '''

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

def to_img(img_ar: asarray):
    '''
    Converts a image pix map to an Image
    '''

    new_img = Image.new(mode='RGBA',
                        size = (len(img_ar[0]), len(img_ar)))
    pix_map = new_img.load()

    for x in range(len(img_ar)):
        for y in range(len(img_ar[0])):
            pix_map[x, y] = img_ar[x][y]

    return new_img


def threshold(img: Image):
    '''
    returns a array only with black or white pixels from a image
    '''

    if img.mode == 'I':
        img = img.convert('RGBA')
    img_ar = asarray(img)
    return _threshold(img_ar)


def compair(data:dict, img_map:list):
    '''
    Do a comparation of all data and the image pix map
    returns a list of percentages
    '''

    for img in data:
        value = 0
        name = img
        img = data[img]['data']
        if not img:continue
        for x in range(len(img)):
            for y in range(len(img[0])):
                if img[x][y] == img_map[x][y]:
                    value += 1
        yield value*100/(len(img[0])*len(img)), name




if __name__ == '__main__':
    if '--help' in argv or '-h' in argv or len(argv) == 1:
        print('''
Usage: ephisem-detect [options] <Image>

Options:
    -h, --help      Show this message.
    -t, --type      Set type of image, must be
                    "middle","top" or "bottom".
        '''.strip())
        exit()

    print(':: Preparing data')
    type_slice = 'middle'
    if '-t' in argv:
        type_slice = argv[argv.index('-t')+1].lower()
    data = prepar_data(type_slice)

    print(':: Preparing image inputed')
    img = Image.open(argv[1])
    img_map = compress_map(threshold(img))

    print('\n\n:: Starting image compair')
    percentages = list(compair(data, img_map))
    for p in range(len(percentages)):
        percentages[p] = percentages[p][0]
    print(f'\n\nEphisem level = {sum(percentages)/len(percentages)}%')
