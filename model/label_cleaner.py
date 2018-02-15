import pandas as pd
from fuzzywuzzy import process


class LabelCleaner(object):
    """

    """
    def __init__(self):
        self.brand_reference = pd.read_csv('model/external_data/brands.csv')

    def clean_labels(self):
        #load raw labels
        raw_labels = pd.read_csv('data/raw_labels.csv')


    def fuzzy_match(self, x, choices, cutoff=50):
        return process.extractOne(x, choices, cutoff)

