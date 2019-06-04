from PIL import Image
import numpy as np
import os
import math

def save_arr_as_img_l(arr, pic_name, file_name, extension):
    img = Image.fromarray(arr).convert(mode='L')
    img.save(file_name + '_' + pic_name + extension)


def save_arr_as_img_rgb(img, pic_name, file_name, extension):
    print(file_name + '_' + pic_name + extension)
    img.save(file_name + '_' + pic_name + extension)


def apply_threshold(value):
        "Returns 0 or 255 depending where value is closer"
        return 255 * math.floor(value/128)

def fs_l(file_name, new_img=None):
    if not new_img:
        new_img = Image.open(file_name)
        new_img = new_img.convert('L')
    pixel = new_img.load()    
    x_lim, y_lim = new_img.size

    for y in range(y_lim):
        for x in range(x_lim):
            oldpixel = pixel[x, y]
            newpixel = apply_threshold(oldpixel)
            pixel[x, y] = newpixel 
            quant_error = oldpixel - newpixel
            
            if x < x_lim - 1:
                pixel[x + 1, y] += round(quant_error * 7 / 16)

            if x > 1 and y < y_lim - 1:
                pixel[x - 1, y + 1] += round(quant_error * 3 / 16)

            if y < y_lim - 1:
                pixel[x, y + 1] += round(quant_error * 5 / 16)

            if x < x_lim - 1 and y < y_lim - 1:
                pixel[x + 1, y + 1] += round(quant_error * 1 / 16)
                
    return new_img


def fs_rgb(file_name):
    new_img = Image.open(file_name)
    new_img = new_img.convert('RGB')
    imgs = new_img.split()
    out = []
    for img in imgs:
        out.append(fs_l(file_name, new_img=img))
    return Image.merge('RGB', out)


def floyd_steinberg(file_name, mode='RGB'):
    print(file_name, mode)
    if mode == 'L':
        return fs_l(file_name)
    else:
        return fs_rgb(file_name)


def bayer_matrix(n, transposed=False):
    return np.array((1 + index_matrix(n, transposed)) / (1 + (n * n)))


def index_matrix(n, transposed=False):
    if n == 2:
        if transposed:
            return np.array([[0, 3], [2, 1]], 'int')
        else:
            return np.array([[0, 2], [3, 1]], 'int')
    else:
        smaller = index_matrix(n >> 1, transposed)
        if transposed:
            return np.bmat([[4 * smaller, 4 * smaller + 3],
                            [4 * smaller + 2, 4 * smaller + 1]])
        else:
            return np.bmat([[4 * smaller,     4 * smaller + 2],
                            [4 * smaller + 3, 4 * smaller + 1]])


def b_l(file_name, order=8, new_img=None):
    if not new_img:
        new_img = Image.open(file_name)
        new_img = new_img.convert('L')
    pixel = new_img.load()    
    x_lim, y_lim = new_img.size
    bm = bayer_matrix(order)

    for y in range(y_lim):
        for x in range(x_lim):
            c = int(pixel[x, y] + 256/2*(bm[x%order][x%order]-0.5))
            if c >=  128:
                pixel[x, y] = 255
            else:
                pixel[x, y] = 0
    return new_img


def b_rgb(file_name, order=8):
    new_img = Image.open(file_name)
    new_img = new_img.convert('RGB')
    imgs = new_img.split()
    out = []
    for img in imgs:
        out.append(b_l(file_name, new_img=img, order=order))
    return Image.merge('RGB', out)


def bayer(file_name, mode='RGB'):
    print(file_name, mode)
    if mode == 'L':
        return b_l(file_name)
    else:
        return b_rgb(file_name)


def dithering(file_name, mode='RGB', alg='floyd_steinberg'):
    if alg == 'bayer':
        return bayer(file_name, mode=mode)
    else:
        return floyd_steinberg(file_name, mode=mode)


file_name = r'D:/test/n2.jpg'
file, ext = os.path.splitext(file_name)

arr = dithering(file_name, mode='RGB', alg='floyd_steinberg')
save_arr_as_img_rgb(arr, 'fs_rgb', file, ext)