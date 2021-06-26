import matplotlib.pyplot as plt
import numpy as np

def read_image(path, scale=True):
    img = plt.imread(path)
    if scale:
        return np.uint8(img*255)
    return img

from PIL import Image

def scale_image(image, scale):
    img = Image.fromarray(np.uint8(image))
    img = img.resize((int(img.width*scale), int(img.height*scale)), Image.NEAREST)
    return np.asarray(img)

def scale_image_up(image):
    return scale_image(image, 2)

def scale_image_down(image):
    return scale_image(image, 0.5)

def extract_validation_patch(image):
    patches = np.asarray(np.hsplit(np.asarray(np.hsplit(image, 7)), 2))[1,1:5]
    return np.concatenate(patches, axis=1)