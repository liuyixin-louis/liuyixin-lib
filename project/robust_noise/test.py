from PIL import Image, ImageFilter
import numpy as np
# image_arr = [0,0,0,0]
# image_arr = np.array(image_arr)
# x=Image.fromarray(image_arr)
x=Image.open("/ssd2/liuyixin04/workspace/test-yixin/rena.png")
# x.filter(ImageFilter.GaussianBlur)
# x.filter(ImageFilter.BLUR)
# x.filter(ImageFilter.MedianFilter)
x.filter(ImageFilter.EDGE_ENHANCE)
x.save(
    'fig.png'
)