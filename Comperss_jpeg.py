from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import scipy.fftpack

# here we convert RGB to YCbCr
def rgb2ycbcr(image, color_pix):
    lst = []
    for item in color_pix :
        # print(item[0])
        r = item [0]
        g = item [1]
        b = item [2]
        y = 16 + (65.738 * r / 256) + (109.057 * g / 256) + (25.064 * b / 256)
        cb = 128 - (37.945 * r / 256) - (74.494 * g / 256) + (112.439 * b / 256)
        cr = 128 + (112.439 * r / 256) - (95.154 * g / 256) - (18.285 * b / 256)
        lst.append((int(y), int(cb), int(cr)))
    image.putdata(lst)
    # image.show()
    subsampling(image)

def subsampling(image) :
    img_width = image.width
    img_height = image.height
    cb = 0
    cr = 0
    for i in range(img_width) :
        for j in range(img_height) :
            y = image.getpixel((i,j))[0]
            if i % 2 == 1 or j % 2 == 1 : 
                cb = image.getpixel((i - (i % 2), j - (j % 2)))[1]
                cr = image.getpixel((i - (i % 2), j - (j % 2)))[2]
                image.putpixel((i,j), (int(y),int(cb), int(cr)))
    # image.show()
    blocking(image)

def blocking(image) : 
    width = image.width
    height = image.height
    image.save("image_after_subsampling.jpg")
    for i in range(0, width, 8) :
        for j in range(0, height, 8) : 
            block = [[0] * 8] * 8
            for b_x in range(i, i + 8) : 
                for b_y in range(j, j + 8) : 
                    if (b_x >= width) or (b_y >= height) : 
                        data = (0, 0, 0)
                    else : 
                        data = image.getpixel((b_x, b_y))
                    block[b_x - i][b_y - j] = data
            print(two_dimentional_DCT(block))
                # print(i, j)
                # for item in arr : 
                #     print(item)

def two_dimentional_DCT(block) : 
    return scipy.fftpack.dct( scipy.fftpack.dct(block, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')
    
img = Image.open('photo1.png')
rgb_image = img.convert('RGB')
rgb_image.save("photo.jpg")
color_pixel = list(rgb_image.getdata())
rgb2ycbcr(rgb_image, color_pixel)
# print(color_pixel)





