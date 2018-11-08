from PIL import Image
import numpy as np


def save_arr_as_img(arr, pic_name, file_name, extension):
    img = Image.fromarray(arr).convert(mode='L')
    img.save(file_name + '_' + pic_name + extension)


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


def gradients(image, type='sobel'):
    type = type.lower()
    print(type)
    if type == 'roberts':  # roberts cross
        Kx = np.array([[1, 0], [0, -1]], np.int32)  # x roberts cross kernel
        Ky = np.array([[0, 1], [-1, 0]], np.int32)  # y roberts cross kernel
        x_grad = convolution2d(image, Kx, 0)
        y_grad = convolution2d(image, Ky, 0)
        print('roberts')
    elif type == 'pewitt':  # pewitt
        Kx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], np.int32)  # x pewitt kernel
        Ky = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], np.int32)  # y pewitt kernel
        x_grad = convolution2d(image, Kx, 0)
        y_grad = convolution2d(image, Ky, 0)
        print('pewitt')
    else:  # sobel
        Kx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], np.int32)  # x pewitt kernel
        Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.int32)  # y pewitt kernel
        x_grad = convolution2d(image, Kx, 0)
        y_grad = convolution2d(image, Ky, 0)
        print('sobel')
    return x_grad, y_grad


def grad_theta(x, y):
    grad = np.hypot(x, y)
    theta = np.arctan2(y, x)
    return grad, theta


def suppression(image, grad):
    m, n = image.shape
    supr = np.zeros((m, n), dtype=np.int32)

    for i in range(1, m - 2):
        for j in range(1, n - 2):
            where = get_angle(grad[i, j])
            try:
                if where == 0:
                    if (image[i, j] >= image[i, j - 1]) and (image[i, j] >= image[i, j + 1]):
                        supr[i, j] = image[i, j]
                elif where == 90:
                    if (image[i, j] >= image[i - 1, j]) and (image[i, j] >= image[i + 1, j]):
                        supr[i, j] = image[i, j]
                elif where == 135:
                    if (image[i, j] >= image[i - 1, j - 1]) and (image[i, j] >= image[i + 1, j + 1]):
                        supr[i, j] = image[i, j]
                elif where == 45:
                    if (image[i, j] >= image[i - 1, j + 1]) and (image[i, j] >= image[i + 1, j - 1]):
                        supr[i, j] = image[i, j]
            except IndexError as e:
                pass
    return supr


def get_angle(angle):
    angle = np.rad2deg(angle) % 180
    if (0 <= angle < 22.5) or (157.5 <= angle < 180):
        angle = 0
    elif 22.5 <= angle < 67.5:
        angle = 45
    elif 67.5 <= angle < 112.5:
        angle = 90
    elif 112.5 <= angle < 157.5:
        angle = 135
    return angle


def threshold(image, low=100, high=200):
    cf = {'weak': np.int32(50), 'strong': np.int32(255)}
    strong_i, strong_j = np.where(image > high)
    weak_i, weak_j = np.where((image >= low) & (image <= high))
    zero_i, zero_j = np.where(image < low)
    image[strong_i, strong_j] = cf.get('strong')
    image[weak_i, weak_j] = cf.get('weak')
    image[zero_i, zero_j] = np.int32(0)
    return image, cf.get('weak')


def tracking(img, weak, strong=255):
    m, n = img.shape
    for i in range(m):
        for j in range(n):
            if img[i, j] == weak:
                try:
                    if ((img[i + 1, j] == strong) or (img[i - 1, j] == strong)
                            or (img[i, j + 1] == strong) or (img[i, j - 1] == strong)
                            or (img[i + 1, j + 1] == strong) or (img[i - 1, j - 1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img


#file_name = r'D:/test/test2'
#file_name = r'D:/test/test1'
#file_name = r'D:/test/test'
file_name = r'D:/test/hype_tweety_bg2'

#ext = r'.jpg'
ext = r'.png'



path = file_name + ext
bw = Image.open(path).convert(mode='L')
image = np.array(bw)
save_arr_as_img(image, 'bw', file_name, ext)

g = gauss_kernel(2, 0.8)
blur = convolution2d(image, g, 0)
save_arr_as_img(blur, 'conv', file_name, ext)

x_grad, y_grad = gradients(blur, type='sobel')
save_arr_as_img(x_grad, 'x_grad', file_name, ext)
save_arr_as_img(y_grad, 'y_grad', file_name, ext)

grad, theta = grad_theta(x_grad, y_grad)
save_arr_as_img(grad, 'grad', file_name, ext)

supr = suppression(grad, theta)
save_arr_as_img(supr, 'supr', file_name, ext)

thres, weak = threshold(supr, low=10, high=40)
save_arr_as_img(thres, 'thres', file_name, ext)

final = tracking(thres, weak, strong=255)
save_arr_as_img(final, 'final', file_name, ext)

print()
