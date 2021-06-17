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
    channels = 1
    if len(image.shape) == 3:
        channels = 3
    image = image.reshape(image.shape[0], image.shape[1], channels)
    assert image.shape == (2404, 8344, channels) or image.shape == (1202, 4172, channels)
    did_i_scale = False
    if image.shape == (1202, 4172, channels):
        image = scale_image_up(np.squeeze(image))
        did_i_scale = True
    image = np.squeeze(image.reshape(2,1202,7,1192,channels)[1,:,1:5,:,:].reshape(1202, -1, channels))
    if did_i_scale:
        image = scale_image_down(image)
    return image