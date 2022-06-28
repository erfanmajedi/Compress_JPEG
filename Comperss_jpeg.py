from pickletools import uint8
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
import scipy.fftpack




standard_luminance_quantization_table = np.array(
[ 16,  11,  10,  16,  24,  40,  51,  61,
  12,  12,  14,  19,  26,  58,  60,  55,
  14,  13,  16,  24,  40,  57,  69,  56,
  14,  17,  22,  29,  51,  87,  80,  62,
  18,  22,  37,  56,  68, 109, 103,  77,
  24,  35,  55,  64,  81, 104, 113,  92,
  49,  64,  78,  87, 103, 121, 120, 101,
  72,  92,  95,  98, 112, 100, 103,  99],dtype=int)

standard_luminance_quantization_table = standard_luminance_quantization_table.reshape([8,8])

standard_chrominance_quantization_table = np.array(
[ 17,  18,  24,  47,  99,  99,  99,  99,
  18,  21,  26,  66,  99,  99,  99,  99,
  24,  26,  56,  99,  99,  99,  99,  99,
  47,  66,  99,  99,  99,  99,  99,  99,
  99,  99,  99,  99,  99,  99,  99,  99,
  99,  99,  99,  99,  99,  99,  99,  99,
  99,  99,  99,  99,  99,  99,  99,  99,
  99,  99,  99,  99,  99,  99,  99,  99],dtype=int)

standard_chrominance_quantization_table = standard_chrominance_quantization_table.reshape([8,8])

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
    dct_coefficients = [[0] * height] * width
    for i in range(0, width, 8) :
        for j in range(0, height, 8) : 
            block = [[0] * 8] * 8
            for block_x_axis in range(i, i + 8) : 
                for block_y_axis in range(j, j + 8) : 
                    if (block_x_axis >= width) or (block_y_axis >= height) : 
                        data = (0, 0, 0)
                    else : 
                        data = image.getpixel((block_x_axis, block_y_axis))
                    block[block_x_axis - i][block_y_axis - j] = data
            dct_coefficients[i][j] = two_dimentional_DCT(block)
    quantized_matrix(dct_coefficients , image) 
            # quantized_matrix(dct_coefficients[i][j], width, height)
            # print(i, j)
                # for item in block : 
                    # print(item)
                    

def two_dimentional_DCT(block) : 
    return scipy.fftpack.dct(scipy.fftpack.dct(block, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')


def quantized_matrix(dct_matrix, img) :
    img_wid = img.width
    img_hei = img.height
    new_block = [[0] * img_hei] * img_wid 
    
    for x in range(0, img_wid, 8) :
        for y in range(0, img_hei, 8) :
            # if x == 0 and y == 424 :
                ycbcr = []
                for z in range(8) :
                    new_ycbcr = []
                    for k in range(8) : 
                        Y = dct_matrix[x][y][z][k][0]
                        Cb = dct_matrix[x][y][z][k][1]
                        Cr = dct_matrix[x][y][z][k][2]
                        y_bar = round(Y / standard_luminance_quantization_table[z][k])
                        cb_bar = round(Cb / standard_chrominance_quantization_table[z][k])
                        cr_bar = round(Cr / standard_chrominance_quantization_table[z][k])
                        ycbcr.append((y_bar, cb_bar, cr_bar))
                    new_ycbcr.append(ycbcr)
                new_block[x][y] = new_ycbcr
                # print(new_ycbcr)




img = Image.open('photo1.png')
rgb_image = img.convert('RGB')
rgb_image.save("photo.jpg")
color_pixel = list(rgb_image.getdata())
rgb2ycbcr(rgb_image, color_pixel)
# print(color_pixel)





