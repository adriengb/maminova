import multiprocessing
import glob
from functools import partial
import random
import pandas as pd
import shutil
import os

class ImageSorter(object):
    """

    """
    def __init__(self, train_size=0.7, seed=42):
        self.train = train_size
        self.seed = seed
        self.labels = pd.read_csv('../data/cleaned_labels.csv')

    def sort(self):
        imagesList = glob.glob("../data/raw/*.jpg")
        random.seed(self.seed)
        random.shuffle(imagesList)
        split_index = int(len(imagesList)*self.train)
        train_images = imagesList[:split_index]
        test_images = imagesList[split_index:]
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(partial(self.__sort__, mode='train'), train_images)
        pool.map(partial(self.__sort__, mode='predict'), test_images)
        pool.close()

    def __sort__(self, img_path, mode):
        img_name = img_path.split('/')[-1]
        brand = list(self.labels.cleaned_brand[self.labels.image_name==img_name])
        if brand:
            directory = '../model/{}/{}'.format(mode, brand[0])
            if not os.path.exists(directory):
                os.makedirs(directory)
            dst = '{}/{}'.format(directory, img_name)
            shutil.copy(img_path, dst)

if __name__ == '__main__':
    transformer = ImageSorter(train_size=0.7)
    transformer.sort()