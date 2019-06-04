from PIL import Image
import numpy as np
import os

def save_arr_as_img_l(arr, pic_name, file_name, extension):
    img = Image.fromarray(arr).convert(mode='L')
    img.save(file_name + '_' + pic_name + extension)


def save_arr_as_img_rgb(img, pic_name, file_name, extension):
    print(file_name + '_' + pic_name + extension)
    img.save(file_name + '_' + pic_name + extension)




def pixelate(file_name, pixelSize=10):
    img = Image.open(file_name)
    img = img.resize((int(img.size[0]/pixelSize), int(img.size[1]/pixelSize)), Image.NEAREST)
    img = img.resize((int(img.size[0]*pixelSize), int(img.size[1]*pixelSize)), Image.NEAREST)
    return img

"""
backgroundColor = (0,)*3
for i in range(0,image.size[0],pixelSize):
  for j in range(0,image.size[1],pixelSize):
    for r in range(pixelSize):
      pixel[i+r,j] = backgroundColor
      pixel[i,j+r] = backgroundColor
"""


file_name = r'D:/test/n2.jpg'
file, ext = os.path.splitext(file_name)

save_arr_as_img_rgb(pixelate(file_name, pixelSize=15), 'pixelated', file, ext)
