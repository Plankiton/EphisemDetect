from util import *

def compare(pxl1, pxl2):
    stage, cat_stage = [], []
    h1, w1 = len(pxl1), len(pxl1[0])
    h2, w2 = len(pxl2), len(pxl2[0])

    # Size comparation
    diference = h1 - h2
    stage.append(100-(diference*100/h2))
    cat_stage.append('height')

    diference = w1 - w2
    stage.append(100-(diference*100/w2))
    cat_stage.append('width')


    # pixel comparation
    line_perc = []
    for x in range(h1):
        count = 0
        history = []
        for y in range(w1):
            if  x < h2 and pxl1[x][y] not in history:
                count += pxl2[x].count(pxl1[x][y])
                history.append(pxl1[x][y])

        line_perc.append((count*100)/w2)
    stage.append(
        sum(line_perc)/len(line_perc)
    )
    cat_stage.append('line')
    del line_perc

    # range pixel comparation
    column_perc = []
    for x in range(h2):
        count = 0
        history = []
        for y in range(w2):
            if x < h1 and pxl2[x][y] not in history:
                count += pxl1[x].count(pxl2[x][y])
                history.append(pxl2[x][y])

        column_perc.append((count*100)/w2)
    stage.append(
        sum(column_perc)/len(column_perc)
    )
    cat_stage.append('column')
    del column_perc

    # pixel to pixel comparation
    count = 0
    hl = h1 - (h1-h2)
    wl = w1 - (w1-w2)
    for x in range(hl):
        for y in range(wl):
            if pxl1[x][y] == pxl2[x][y]:
                count += 1
    stage.append( (count * 100) / (hl * wl) )
    cat_stage.append('item_to_item')


    # pixel in list comparation
    count = []
    for x in range(h1):
        for y in range(w1):
            for x2 in range(h2):
                if pxl1[x][y] not in history:
                    count.append(
                        pxl2[x2].count(pxl1[x][y])
                    )
    print((sum(count)*100)/w2*h2)

    cat_stage.append('item_in_list')

    print(*(f'{cat_stage[i]}: {stage[i]}\n' for i in r(len(stage))), sep = '')
    return sum(stage)/len(stage)

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


def do_lbp_on_pix_map(pix_map, only_thershold = False):
    c = 0
    new_pix_map = []
    for x in r(0, len(pix_map), 3):
        limited_pix_list = pix_map[x:x+3]

        new_pix_map.append([])
        for y in r(0, len(pix_map[0]), 3):
            local_pix_range = [c[y:y+3] for c in limited_pix_list]

            if only_thershold and len(local_pix_range) == 3 \
                    and len(local_pix_range[0]) == 3:
                pixel = local_binary_patt(local_pix_range)
                pix_map[x+1][y+1] = pixel

            elif len(local_pix_range) == 3 \
                    and len(local_pix_range[0]) == 3:
                pixel = local_binary_patt(local_pix_range)
                new_pix_map[c].append(pixel)

        if new_pix_map[c] == []:
            del new_pix_map[c]
        else:
            c += 1
    return  pix_map if only_thershold else new_pix_map


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
