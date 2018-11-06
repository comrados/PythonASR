from PIL import Image
import argparse
import sys


def calc_new_size(ratio, img):
    """
    Calculates new dimensions.

    :param ratio: ration of shrinking/magnification
    :param img: image
    :return: new dimensions
    """
    if ratio > 0:
        return int(ratio * img.height), int(ratio * img.width)
    else:
        print("Wrong ratio, must be grater than 0, current value: ", ratio)
        sys.exit(2)


def num_to_char_4(num, inverted):
    """
    Recoding to 4 shades

    :param num: original pixel shade
    :param inverted: inverted colors or not
    :return: character
    """
    if inverted:
        dic = {3: r' ', 2: r'░', 1: r'▓', 0: r'█'}
    else:
        dic = {0: r' ', 1: r'░', 2: r'▓', 3: r'█'}
    if num < 64:
        return dic.get(3)
    if num < 128:
        return dic.get(2)
    if num < 192:
        return dic.get(1)
    if num < 256:
        return dic.get(0)


def num_to_char_3(num, inverted):
    """
    Recoding to 3 shades

    :param num: original pixel shade
    :param inverted: inverted colors or not
    :return: character
    """
    if inverted:
        dic = {2: r'░', 1: r'▓', 0: r'█'}
    else:
        dic = {0: r'░', 1: r'▓', 2: r'█'}
    if num < 128:
        return dic.get(2)
    if num < 192:
        return dic.get(1)
    if num < 256:
        return dic.get(0)


def get_pixel(image, i, j):
    """
    Gets pixel from the position [i,j]

    :param image: image
    :param i: i
    :param j: j
    :return: pixel
    """
    width, height = image.size
    if i > width or j > height:
        return None
    pixel = image.getpixel((i, j))
    return pixel


def convert_ascii(image, shades, invert):
    """
    Converts pixel monochrome image to array of chars of 3 or 4 shades

    :param image: image
    :param shades: number of shades
    :param invert: inverted colors or not
    :return:
    """
    width, height = image.size
    new = [['' for x in range(height)] for y in range(width)]
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            if shades == 3:
                new[i][j] = num_to_char_3(pixel, invert)
            if shades == 4:
                new[i][j] = num_to_char_4(pixel, invert)
    new = list(zip(*new[::-1]))
    return [x[::-1] for x in new]


def output(asc, file, co):
    """
    Writes text file wih chars

    :param asc: array of characters
    :param file: file to write to
    """
    file = open(file, "wb+")
    for i in range(len(asc)):
        line = ''
        for j in range(len(asc[0])):
            line += asc[i][j]
            file.write(asc[i][j].encode('utf8'))
        file.write(b'\r\n')
        if co:
            print(line)
    file.flush()
    file.close()


def main(args):
    img = Image.open(args.pl).convert(mode='L')
    print("Opened image:", args.pl)
    h, w = calc_new_size(args.ratio, img)
    img = img.resize((w, h))
    if args.verbose:
        print(f"New sizes: h={h}, w={w}")
    asc = convert_ascii(img, args.shades, args.invert)
    if args.verbose:
        inv = 'not'
        if args.invert:
            inv = ''
        print(f"Converted to image with {int(args.shades)} shades, colors {inv} inverted")
    output(asc, args.pst, args.console_out)
    print("Text saved to:", args.pst)
    if args.psp is not None:
        img.save(args.psp)
        print("Transformed image saved to:", args.psp)


def parse_args(argv):
    parser = argparse.ArgumentParser(description='''Сука, блядь, пидор. 
    Винишь ли ты меня в слепоте мысли, пидор, сука, блядь? 
    Я, блядь, вижу, сука, образ, блядь, пидорас, являющийся выражением, ёбаный твой рот, эмоций, блядь. 
    Понимаешь меня? Блядь, да проще тебе ебало набить.''', prog='pic_to_ascii.py')
    parser.add_argument('pl', help='Path to the original picture', metavar='<path-load>')
    parser.add_argument('pst', help='Path to save text', metavar='<path-save-txt>')
    parser.add_argument('-psp', help='Path to save picture', metavar='<path-save-pic>', default=None)
    parser.add_argument('-v', '--verbose', help='Verbose output.', default=False, action='store_true')
    parser.add_argument('-i', '--invert', help='Invert colors', default=False, action='store_true')
    parser.add_argument('-s', '--shades', help='Number of shades', default=3, choices=[3, 4], type=float,
                        metavar='<shades>')
    parser.add_argument('-co', '--console-out', help='Console output of ascii-art', default=False, action='store_true')
    parser.add_argument('-r', '--ratio', help="Image shrinking/enlargement coefficient, must be grater than 0",
                        default=1, type=float, metavar='<ratio>')
    try:
        argp = parser.parse_args(argv)
        return argp
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
