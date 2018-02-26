import multiprocessing
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

    def sort(self, min_volume=400):
        random.seed(self.seed)
        brands = pd.DataFrame(self.labels.cleaned_brand.value_counts())
        accepted_brands = list(brands[brands.cleaned_brand > min_volume].index)
        for brand in accepted_brands:
            directory_train = '../model/data_model/train/{}'.format(brand)
            directory_validation = '../model/data_model/validation/{}'.format(brand)
            if not os.path.exists(directory_train):
                os.makedirs(directory_train)
            if not os.path.exists(directory_validation):
                os.makedirs(directory_validation)
            imagesList = list(self.labels[self.labels.cleaned_brand==brand].image_name)
            random.shuffle(imagesList)
            split_index = int(len(imagesList) * self.train)
            train_images = imagesList[:split_index]
            test_images = imagesList[split_index:]
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            pool.map(partial(self.__sort__, mode='train', brand=brand), train_images)
            pool.map(partial(self.__sort__, mode='validation', brand=brand), test_images)
            pool.close()

    def __sort__(self, img_name, mode, brand):
        img_path = '../data/raw/{}'.format(img_name)
        dst = '../model/data_model/{}/{}/{}'.format(mode, brand,img_name)
        try:
            shutil.copy(img_path, dst)
        except:
            print(img_path)

if __name__ == '__main__':
    transformer = ImageSorter(train_size=0.8)
    transformer.sort()