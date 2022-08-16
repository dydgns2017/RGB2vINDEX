# %%
import cv2 as cv
import matplotlib.pyplot as plt
from RGB2GREEN import *
# %%
result = RGB2vNDVI(["dataset/1ec574cf1d66c4d9d62f5e4b3c2c1068.png"])
print(result[0].shape)
plt.imshow(result[0], cmap="RdYlGn")
