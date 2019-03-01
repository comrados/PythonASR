from PIL import Image
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

file_name = r'D:/test/test1.jpg'
file_name1 = r'D:/test/hype_tweety_bg2.png'

img1o = Image.open(file_name).convert(mode='RGB')
print(img1o.size)
img2o = Image.open(file_name1).convert(mode='RGB')
print(img2o.size)

img1 = np.array(img1o.convert(mode='L'))
img2 = np.array(img2o.convert(mode='L'))

f1 = fftpack.fftshift(fftpack.fft2(img1))
f2 = fftpack.fftshift(fftpack.fft2(img2))

img1f = Image.fromarray(np.round(np.real(fftpack.ifft2(fftpack.ifftshift(f1)))))
img2f = Image.fromarray(np.round(np.real(fftpack.ifft2(fftpack.ifftshift(f2)))))

img1f.show()
