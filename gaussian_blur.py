from PIL import Image
import numpy as np


def gauss_kernel(k, sig):
    l = 2 * k + 1
    ax = np.arange(-l // 2 + 1., l // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx ** 2 + yy ** 2) / (2. * sig ** 2))
    return kernel / np.sum(kernel)


def convolution2d(image, kernel, bias):
    m, n = kernel.shape
    if m == n:
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y, x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i + m, j:j + m] * kernel) + bias
    return new_image


#file_name = r'D:/test/test2'
#file_name = r'D:/test/test1'
#file_name = r'D:/test/test'
file_name = r'D:/test/hype_tweety_bg2'

#ext = r'.jpg'
ext = r'.png'

path = file_name + ext
img = Image.open(path).convert(mode='RGB')

red, green, blue, *rest = img.split()

g = gauss_kernel(9, 9)

blur_red = convolution2d(np.array(red), g, 0)
blur_green = convolution2d(np.array(green), g, 0)
blur_blue = convolution2d(np.array(blue), g, 0)

reds = Image.fromarray(blur_red).convert(mode='L')
blues = Image.fromarray(blur_blue).convert(mode='L')
greens = Image.fromarray(blur_green).convert(mode='L')

new_img = Image.merge(img.mode, (reds, greens, blues, *rest))

new_img.show()

