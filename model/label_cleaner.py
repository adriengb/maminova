import pandas as pd
from fuzzywuzzy import process

def fuzzy_match(x, choices, cutoff):
    best_match = process.extractOne(x, choices=choices, score_cutoff=cutoff)
    if best_match:
        return best_match[0]

class LabelCleaner(object):
    """

    """
    def __init__(self):
        self.brand_reference = list(pd.read_csv('../model/external_data/brands.csv', header=None, names=['brand']).brand)

    def clean_labels(self):
        #load raw labels
        raw_labels = pd.read_csv('../data/raw_labels.csv')
        #fuzzy match brands
        raw_labels['cleaned_brand'] = raw_labels['brand'].apply(fuzzy_match, args=(self.brand_reference, 50))
        #remove unknown brands
        new_labels = raw_labels[raw_labels.cleaned_brand.notnull()][['cleaned_brand', 'image_name']]
        new_labels.to_csv('../data/cleaned_labels.csv', index=False)




if __name__ == '__main__':
    cleaner = LabelCleaner()
    cleaner.clean_labels()
