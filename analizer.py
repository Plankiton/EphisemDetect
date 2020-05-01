from image import get_pix_map, Image
from util import *

def compare(pxl1, pxl2):
    try:
        h1, w1 = len(pxl1), len(pxl1[0])
        h2, w2 = len(pxl2), len(pxl2[0])
    except:return [0]

    hl = h1 - (h1-h2)
    wl = w1 - (w1-w2)

    # Size comparation
    diference = h1 - h2
    yield 100-(diference*100/h2)
    #stage.append(100-(diference*100/h2))
    #cat_stage.append('height')

    diference = w1 - w2
    yield 100-(diference*100/w2)
    #stage.append(100-(diference*100/w2))
    #cat_stage.append('width')

    swap1, swap2 = [], []
    for x in range(hl):
        swap2.append([])
        swap1.append([])
        for y in range(wl):
            try:
                swap2[y].append(pxl2[y][x])
                swap1[y].append(pxl1[y][x])
            except:continue

    # line pixel comparation
    line_perc = []
    for x in range(h1):
        count = 0
        history = []
        for y in range(w1):
            if  x < h2 and pxl1[x][y] not in history:
                count += pxl2[x].count(pxl1[x][y])
                history.append(pxl1[x][y])

        line_perc.append((count*100)/w2)
    yield sum(line_perc)/len(line_perc)
    #stage.append(
    #    sum(line_perc)/len(line_perc)
    #)
    #cat_stage.append('line-line')

    line_perc = []
    for x in range(h2):
        count = 0
        history = []
        for y in range(w2):
            if x < h1 and pxl2[x][y] not in history:
                count += pxl1[x].count(pxl2[x][y])
                history.append(pxl2[x][y])

        line_perc.append((count*100)/w2)
    yield sum(line_perc)/len(line_perc)
    #stage.append(
    #    sum(line_perc)/len(line_perc)
    #)
    #cat_stage.append('line-line (2 on 1)')
    del line_perc


    # column pixel comparation
    column_perc = []
    for x in range(h1):
        count = 0
        history = []
        for y in range(w1):
            try:
                if x < h2 and swap1[x][y] not in history:
                    count += swap2[x].count(swap1[x][y])
                    history.append(swap1[x][y])
            except:break

        column_perc.append((count*100)/w2)
    yield sum(column_perc)/len(column_perc)
    #stage.append(
    #    sum(column_perc)/len(column_perc)
    #)
    #cat_stage.append('col-col')

    column_perc = []
    for x in range(h2):
        count = 0
        history = []
        for y in range(w2):
            try:
                if x < h1 and swap2[x][y] not in history:
                    count += swap1[x].count(swap2[x][y])
                    history.append(swap2[x][y])
            except:break

        column_perc.append((count*100)/w2)
    yield sum(column_perc)/len(column_perc)
    #stage.append(
    #    sum(column_perc)/len(column_perc)
    #)
    #cat_stage.append('col-col (2 on 1)')
    del column_perc


    # pixel to pixel comparation
    count = 0
    for x in range(hl):
        for y in range(wl):
            try:
                if pxl1[x][y] == pxl2[x][y]:
                    count += 1
            except:break
    yield  (count * 100) / (hl * wl)
    #stage.append( (count * 100) / (hl * wl) )
    #cat_stage.append('item-item')

    #print(*(f'{cat_stage[i]}: {stage[i]}\n' for i in r(len(stage))), sep = '')
    #return sum(stage)/len(stage)

def _local_binary_patt_list(pixel_list: list):
    height = len(pixel_list)
    width = len(pixel_list[0])

    thershold = \
        pixel_list [height//2] [width//2]

    lbp = [[0 for y in range(height)]
           for x in range(width)]
    for x in range(height):
        for y in range(width):
            pixel = pixel_list[x][y]
            neighbour_pixels = height*width - 1

            if not (x, y) == (height//2, width//2):
                lbp[x][y] = 1 if (
                    ((pixel - thershold) * 2 ** neighbour_pixels) >= 0
                ) else 0
            else:
                lbp[x][y] = None

    return lbp

def local_binary_patt(pixel_list: list) -> int:
    lbp_list = _local_binary_patt_list(pixel_list)

    binary = ''
    sequence = (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 1),
        (2, 0),
        (1, 0),
    )
    for x,y in sequence:
        binary += str(lbp_list[x][y])
    return eval(f'0x{binary}')


def media(num_list):
    total = 0
    for num in num_list:
        total += num
    return total/len(num_list)


def get_lbp(img: Image.Image, pix_map = None):
    if 'rgb' in img.mode.lower():
        img = img.convert(mode='I', matrix=None, dither=None, palette=0, colors=256)
    pix_map = img.load()

    c = 0
    new_pix_map = []
    for x in r(0, img.height, 3):

        new_pix_map.append([])
        for y in r(0, img.width, 3):
            try:
                local_pix_range = [[
                    pix_map[i, j] for j in range(y, y+3)
                ] for i in range(x, x+3)]
            except:
                break

            if len(local_pix_range) == 3 \
                    and len(local_pix_range[0]) == 3:
                pixel = local_binary_patt(local_pix_range)
                new_pix_map[c].append(pixel)

        if new_pix_map[c] == []:
            del new_pix_map[c]
        else:
            c += 1

    return new_pix_map


if __name__ == '__main__':
    from sys import argv as args
    from image import *

    img = Image.open(args[1])
    img_pix_map = img.load()

    pix_map = [[None for j in r(img.height)]
                   for i in r(img.width)]
    for x in range(img.width):
        for y in range(img.height):
            pix_map[x][y] = img_pix_map[x, y]

    c = 0
    lbp_pix_map = do_lbp_on_pix_map(pix_map)
    new_img = Image.new('RGBA', size = (
        len(lbp_pix_map), len(lbp_pix_map[0])
    ))

    new_pix_map = new_img.load()
    for x, y, pixel in get_pix_map(lbp_pix_map):
        new_pix_map[x, y] = pixel

    img.show()
    new_img.show()
