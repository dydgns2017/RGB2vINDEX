import argparse
import os, glob
vipshome = "vips-dev-8.12\\bin" ## u will be modify this line
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import numpy as np
import pyvips
import cv2
from lib.colormaps import RdYlGn_lut
from lib.common import *

def RGB2VARI(images):
    VARI_images = []
    for img in images:
        image = pyvips.Image.new_from_file(f"{img}")
        R,G,B = splitChannel(image)
        VARI = (G-R) / (G+R-B)
        VARI_images.append(VARI)
    return VARI_images

def RGB2GLI(images):
    GLI_images = []
    for img in images:
        image = pyvips.Image.new_from_file(f"{img}")
        R,G,B = splitChannel(image)
        GLI = (2.0 * G - R - B) / (2.0 * G + R + B)
        GLI_images.append(GLI)
    return GLI_images

def RGB2TGI(images):
    TGI_images = []
    for img in images:
        image = pyvips.Image.new_from_file(f"{img}")
        R,G,B = splitChannel(image)
        TGI = -0.5 * (190 * (R - G) - 120 * (R - B))
        TGI_images.append(TGI)
    return TGI_images

def RGB2VIgreen(images):
    VIgreen_images = []
    for img in images:
        image = pyvips.Image.new_from_file(f"{img}")
        R,G,B = splitChannel(image)
        VIgreen = (G-R)/(G+R)
        VIgreen_images.append(VIgreen)
    return VIgreen_images

def RGB2vNDVI(images):
    vNDVI_images = []
    for img in images:
        image = pyvips.Image.new_from_file(f"{img}")
        R,G,B = splitChannel(image)
        vNDVI = 0.5268*((R**-0.1294) * (G**0.3389) * (B**-0.3118))
        vNDVI_images.append(vNDVI)
    return vNDVI_images

def fileSave(convert, origin):
    OUT = os.path.join("./", "output")
    if ( not os.path.exists(OUT) ):
        os.mkdir(OUT)
    MERGE = os.path.join("./", "merge")
    if ( not os.path.exists(MERGE) ):
        os.mkdir(MERGE)
    for i,img in enumerate(convert):
        ## visualization
        rdylgn_image = pyvips.Image.new_from_array(RdYlGn_lut).bandfold()
        result = img.maplut(rdylgn_image)
        result.write_to_file(f"{OUT}/{i+1}.jpg")
    for i,img in enumerate(origin): ## image channel merge
        img = cv2.imread(img, cv2.IMREAD_UNCHANGED).astype("uint8")
        B,G,R = cv2.split(img)
        convert_image = np.asarray(convert[i]).astype("uint8")
        merge = np.dstack((B,G,R, convert_image)) ## numpy channel merge
        if (merge.shape[-1]>=4):
            ## npy save
            np.save(f"{MERGE}/{i+1}.npy", merge, allow_pickle=True)
        else:
            cv2.imwrite(f"{MERGE}/{i+1}.png", merge)

def getImages(DATASET_PATH):
    types = ('*.png', '*.jpg', '*.jpeg') # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(f"{DATASET_PATH}/{files}"))
    return files_grabbed

def splitChannel(image):
    R,G,B = image.bandsplit()
    return (R,G,B)

def applyIndex(convert):
    # normalization
    histograms = [result_histogram(image) for image in convert]
    results = []
    for i, img in enumerate(histograms):
        min_max = find_clipped_min_max(img, convert[i].min(), convert[i].max())
        nmin = min_max['nmin']
        nmax = min_max['nmax']
        result = ((convert[i]-nmin) / (nmax-nmin)) * 256
        results.append(result)
    return results

def main(F, DATASET_PATH):
    images = getImages(DATASET_PATH)
    images_convert = globals()[f"RGB2{F}"](images)
    fileSave(applyIndex(images, images_convert), images)
    
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
