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
        self.labels = pd.read_csv('../model/label_prep/output.csv')
        self.correspondance = self.labels[['model', 'brand']].drop_duplicates().set_index('model').to_dict(orient='index')

    def sort(self, min_volume=200, sort_by='brand'):
        random.seed(self.seed)
        models = pd.DataFrame(self.labels.model.value_counts())
        for model in models.index:
            brand = self.correspondance[model]['brand']
            print(brand, model)
            accepted_models = list(models[models.model > min_volume].index)
            directory_train = '../model/data_model/train/{}'.format(brand)
            directory_validation = '../model/data_model/validation/{}'.format(brand)
            if not os.path.exists(directory_train):
                os.makedirs(directory_train)
            if not os.path.exists(directory_validation):
                os.makedirs(directory_validation)
            imagesList = list(self.labels[self.labels.model==model].image_name)
            random.shuffle(imagesList)
            split_index = int(len(imagesList) * self.train)
            train_images = imagesList[:split_index]
            test_images = imagesList[split_index:]
            pool = multiprocessing.Pool(multiprocessing.cpu_count())
            pool.map(partial(self.__sort__, mode='train', brand=brand), train_images)
            pool.map(partial(self.__sort__, mode='validation', brand=brand), test_images)
            pool.close()


    def __sort__(self, img_name, mode, brand):
        img_path = '../data/raw_{}/{}'.format(brand, img_name)
        dst = '../model/data_model/{}/{}/{}'.format(mode, brand, img_name)
        try:
            shutil.copy(img_path, dst)
        except:
            print('ko')

if __name__ == '__main__':
    transformer = ImageSorter(train_size=0.8)
    transformer.sort()