r = range

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
    return int(binary, 2)


def media(num_list):
    total = 0
    for num in num_list:
        total += num
    return total/len(num_list)


if __name__ == '__main__':
    from sys import argv as args
    from image import *

    img = Image.open(args[1])

    img_pix_map = [[None for j in r(img.height)]
                   for i in r(img.width)]
    for x, y, shade_of_gray in get_normalized(img):
        img_pix_map[x][y] = shade_of_gray

    c = 0
    new_pixel_list = []
    for x in r(0, img.width, 3):
        lines = img_pix_map[x:x+3]
        new_pixel_list.append([])
        for y in r(0, img.height, 3):
            columns = [c[y:y+3] for c in lines]
            if len(columns) == 3 and len(columns[0]) == 3:
                pixel = local_binary_patt(columns)
            new_pixel_list[c].append(pixel)
        c += 1
    del c

    new_img = Image.new('RGBA', size = (len(new_pixel_list), len(new_pixel_list[0])))
    new_img_pix_map = new_img.load()
    for x in range(new_img.width):
        for y in range(new_img.height):
            new_img_pix_map[x, y] = tuple([new_pixel_list[x][y]
                                           for i in range(3)])


    img.show()
    new_img.show()
