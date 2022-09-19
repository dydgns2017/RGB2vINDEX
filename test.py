# %%
import cv2 as cv
import matplotlib.pyplot as plt
from RGB2GREEN import *
from PIL import Image
# %%
image = "dataset/1ec574cf1d66c4d9d62f5e4b3c2c1068.png"
VIgreen = RGB2VIgreen([image])
GLI = RGB2GLI([image])
VARI = RGB2VARI([image])
vNDVI = RGB2vNDVI([image])
TGI = RGB2TGI([image])

imgs = [VIgreen[0], GLI[0], VARI[0], vNDVI[0], TGI[0]]
title_ar = ["VIgreen", "GLI", "VARI", "vNDVI", "TGI"]
# %%
plt.rcParams['figure.figsize'] = (15.0, 8.0)
rows = 3 
columns = 2
for i in range(5) : 
    image_index = i + 1     # image index 
    ttitle = title_ar[i]
    plt.subplot(rows, columns, image_index) # subplot 
    plt.title(ttitle)   # title 
    # // plt.axis('off')
    plt.xticks([])  # x = None 
    plt.yticks([])  # y = None
    plt.imshow(imgs[i], cmap="RdYlGn")
plt.show()
# %%
