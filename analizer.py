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

def do_lbp_on_pix_map(pix_map):
    c = 0
    new_pix_map = []
    for x in r(0, img.width, 3):
        limited_pix_list = pix_map[x:x+3]

        new_pix_map.append([])
        for y in r(0, img.height, 3):
            local_pix_range = [c[y:y+3] for c in limited_pix_list]

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
    for x, y, gray_shade in get_gray_shade(img):
        pix_map[x][y] = gray_shade

        # img_pix_map[x, y] = tuple([
        #   int(gray_shade) for i in r(3)
        # ])

    c = 0
    new_pix_map = do_lbp_on_pix_map(pix_map)
    new_img = Image.new('RGBA', size = (
        len(new_pix_map), len(new_pix_map[0])
    ))
    new_img_pix_map = new_img.load()

    for x, y, pixel in get_pix_map(new_pix_map):
        new_img_pix_map[x, y] = pixel

    new_img.show()
    img.show()
