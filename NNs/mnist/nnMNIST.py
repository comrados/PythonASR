import struct
import numpy as np
import matplotlib.pyplot as plt
import sys
from mnist.nnOCR import nnOCR

train_img = r'mnist\datasets\train-images'
train_lab = r'mnist\datasets\train-labels'
test_img = r'mnist\datasets\test-images'
test_lab = r'mnist\datasets\test-labels'


def open_file(path):
    try:
        file = open(path, 'rb')
        return file
    except FileNotFoundError:
        print("Can't open file", path)
        sys.exit(2)


def get_img_prop(file):
    file.seek(0, 0)
    mag = struct.unpack('>I', file.read(4))[0]
    file.seek(4, 0)
    size = struct.unpack('>I', file.read(4))[0]
    file.seek(8, 0)
    row = struct.unpack('>I', file.read(4))[0]
    file.seek(12, 0)
    col = struct.unpack('>I', file.read(4))[0]
    return mag, size, row, col


def get_lab_prop(file):
    file.seek(0, 0)
    mag = struct.unpack('>I', file.read(4))[0]
    file.seek(4, 0)
    size = struct.unpack('>I', file.read(4))[0]
    return mag, size


def get_img_item(file, item, rows, cols):
    offset = 16 + item * rows * cols
    file.seek(offset, 0)
    return file.read(rows * cols)


def get_lab_item(file, item):
    offset = 8 + item
    file.seek(offset, 0)
    return file.read(1)


def get_img_and_label(tii, tli, n):
    magi, sizei, rowi, coli = get_img_prop(tii)
    magl, sizel = get_lab_prop(tli)
    if (sizei == sizel) and (n < sizei):
        imgr = np.array(list(get_img_item(tii, n, rowi, coli))).reshape((28, 28))
        labr = struct.unpack('b', get_lab_item(tli, n))[0]
        return imgr, labr
    else:
        print('Wrong files or wrong index')
        sys.exit(2)


def draw_number(imgi, labi):
    plt.title("That's {label}".format(label=labi))
    plt.imshow(imgi, cmap='binary')
    plt.show()


def get_expected_lab(labi):
    arr = [0 for i in range(10)]
    arr[labi] = 1
    return arr


def load_data(tii, tli, n, offset=0):
    out = []
    for i in range(offset, offset + n):
        pixels, label = get_img_and_label(tii, tli, i)
        out.append((np.reshape(pixels/255, (784, 1)), np.reshape(get_expected_lab(label), (10, 1))))
    return out


tri = open_file(train_img)
trl = open_file(train_lab)
tsi = open_file(test_img)
tsl = open_file(test_lab)

train_data = load_data(tri, trl, 50000)
valid_data = load_data(tri, trl, 10000, offset=50000)
test_data = load_data(tsi, tsl, 10000)

img, lab = get_img_and_label(tri, trl, 500)
img = np.array(img).flatten() / 255
# draw_number(img, lab)

x = nnOCR(learn_rate=0.5, layers=[784, 75, 25, 10], model='model2.json', dropout=0.5)

x.train(train_data, 5, 250, test_data=valid_data)

x.save_model('model2.json')
