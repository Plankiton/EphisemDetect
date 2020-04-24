def _local_binary_patt_list(pixel_list: list):
    height = len(pixel_list)
    width = len(pixel_list[0])

    if height < 3 or width < 3:
        raise IndexError

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

    img_rgb_matrix = []
    for x in range(img.width):
        img_rgb_matrix.append([])
        for y in range(img.height):
            img_rgb_matrix[x].append(None)
    print(img_rgb_matrix)

    for x, y, rgb in get_color_matrix(img):
        img_rgb_matrix[x][y] = media(rgb)
        print(img_rgb_matrix[x][y], end = '\n' if x >= img.width else ' ')
