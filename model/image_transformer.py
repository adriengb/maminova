import multiprocessing
import glob
import cv2
import numpy as np
from config import IMAGE_RESOLUTION, IMAGE_INPUT_DIR, IMAGE_OUTPUT_DIR
import matplotlib.pyplot as plot

class ImageTransformer(object):
    """

    """
    def __init__(self):
        self.resolution = IMAGE_RESOLUTION
        self.input_dir = IMAGE_INPUT_DIR
        self.output_dir = IMAGE_OUTPUT_DIR

    def resize(self):
        imagesList = glob.glob("../data/raw/*.jpg")
        print(imagesList)
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(self.__resize__, imagesList)
        pool.close()

    def __resize__(self, img):
        image = cv2.imread(img)
        resized = cv2.resize(image, self.resolution)
        #use swapaxes to convert image to Keras' format
        image_convert = np.swapaxes(np.swapaxes(resized, 1, 2), 0, 1)

if __name__ == '__main__':
    transformer = ImageTransformer()
    transformer.resize()