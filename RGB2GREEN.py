import argparse
from posixpath import split
import cv2 as cv
import os, glob
import numpy as np


def RGB2VARI(images):
    # range : -1 ~ 1
    VARI_images = []
    for img in images:
        image = cv.imread(f"{img}", cv.IMREAD_UNCHANGED).astype("float64")
        R,G,B = splitChannel(image)
        VARI = (G-R) / (G+R-B)
        VARI_images.append(VARI)
    return VARI_images

def RGB2GLI(images):
    # range : -1 ~ 1
    GLI_images = []
    for img in images:
        image = cv.imread(f"{img}", cv.IMREAD_UNCHANGED).astype('float64')
        R,G,B = splitChannel(image)
        GLI = (G-R)+(G-B) / (2*G)+R+B
        GLI_images.append(GLI)
    return GLI_images

def RGB2TGI(images):
    TGI_images = []
    for img in images:
        image = cv.imread(f"{img}", cv.IMREAD_UNCHANGED).astype('float64')
        R,G,B = splitChannel(image)
        TGI = (G - 0.39) * (R - 0.61) * B
        TGI_images.append(TGI)
    return TGI_images

def RGB2VIgreen(images):
    VIgreen_images = []
    for img in images:
        image = cv.imread(f"{img}", cv.IMREAD_UNCHANGED).astype('float64')
        R,G,B = splitChannel(image)
        VIgreen = (G-R)/(G+R)
        VIgreen_images.append(VIgreen)
    return VIgreen_images

def RGB2vNDVI(images): # O
    vNDVI_images = []
    for img in images:
        image = cv.imread(f"{img}", cv.IMREAD_UNCHANGED).astype("float64")
        R,G,B = splitChannel(image)
        R = np.where(R==0, 1, R)
        B = np.where(B==0, 1, B)
        vNDVI = 0.5268*((R**-0.1294) * (G**0.3389) * (B**-0.3118))
        vNDVI_images.append(vNDVI)
    return vNDVI_images

def fileSave(merge_files, files):
    OUT = os.path.join("./", "output")
    if ( not os.path.exists(OUT) ):
        os.mkdir(OUT)
    MERGE = os.path.join("./", "merge")
    if ( not os.path.exists(MERGE) ):
        os.mkdir(MERGE)
    for i,img in enumerate(files):
        cv.imwrite(f"{OUT}/{i+1}.jpg", img)
    for i,img in enumerate(merge_files):
        cv.imwrite(f"{MERGE}/{i+1}.png", img)

def getImages(DATASET_PATH):
    types = ('*.png', '*.jpg', '*.jpeg') # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(f"{DATASET_PATH}/{files}"))
    return files_grabbed

def splitChannel(image):
    B,G,R = cv.split(image)
    return (R,G,B)

def mergeChannel(images, images_convert):
    merge_files = []
    for i,img in enumerate(images):
        src_image = cv.imread(img).astype("float64")
        R,G,B = splitChannel(src_image)
        P = images_convert[i]
        merge_image = cv.merge((B,G,R,P))
        merge_files.append(merge_image)
    return merge_files

def main(F, DATASET_PATH):
    images = getImages(DATASET_PATH)
    images_convert = globals()[f"RGB2{F}"](images)
    merge_files = mergeChannel(images, images_convert)
    print(merge_files[0])
    fileSave(merge_files, images_convert)
    
if __name__ == "__main__":
    np.seterr(divide='ignore', invalid='ignore')
    parser = argparse.ArgumentParser(prog="RGB2GREEN.py")
    parser.add_argument("--generate", type=str)
    parser.add_argument("--datasets", type=str)
    opt = parser.parse_args()
    F = opt.generate
    D = os.path.join("./", opt.datasets) # relative path
    assert F in ["TGI", "VARI", "GLI" , "VIgreen", "vNDVI"], "not founded generate option, --generate TGI|VARI|GLI|VIgreen|vNDVI"
    main(F, D)