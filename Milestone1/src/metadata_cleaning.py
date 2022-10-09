import os
import ast

import numpy as np
import pandas as pd
import datetime
import operator, functools

def parse_through_data(data_frame):
    df = drop_unnecessary_columns(data_frame)
    #df = drop_duplicates(df)
    df = drop_bad_rows(data_frame)
    df = transform_data(df)
    return df


def transform_isbn(data_frame):
    # data_frame[data_frame['details'].apply(lambda x: 'Page Numbers Source ISBN:' in x)]
    data_frame['ISBN'] = data_frame['details'].apply(
        lambda x: x['Page Numbers Source ISBN:'].replace('ISBN-10: ', '')
        if 'Page Numbers Source ISBN:' in x else np.nan)
    return data_frame


#Creates columns no_pages and publication_date
def transform_details(data_frame):
    data_frame['no_pages'] = data_frame['details']. \
        apply(lambda x: int(ast.literal_eval(x)['Print Length:'].split(' ')[0]) if 'Print Length:' in ast.literal_eval(x) else -1)
    #data_frame['Publisher'] = data_frame['details']. \
    #    apply(lambda x: x['Publisher:'].split(';')[0] if 'Publisher:' in x else np.nan)
    data_frame['publication_date'] = data_frame['details'].apply(
        lambda x: datetime.datetime.strptime(ast.literal_eval(x)['Publication Date:'], '%B %d, %Y').date()
        if 'Publication Date:' in ast.literal_eval(x) else '')
    #data_frame['Language'] = data_frame['details']. \
    #    apply(lambda x: x['Language:'] if 'Language:' in x else np.nan)
    data_frame = data_frame.drop(['details'], axis=1)
    return data_frame

#Reorganize columns
def reorganize_data(data_frame):
    # cols = data_frame.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    # data_frame = data_frame[cols]
    return data_frame[['asin', 'title', 'brand', 'category', 'publication_date', 'no_pages']]

def trim_data(data_frame):
    data_frame['title'] = data_frame['title'].apply(lambda x: str(x).strip())
    data_frame['category'] = data_frame['category'].apply(lambda x: str(x).strip())
    data_frame['brand'] = data_frame['brand'].apply(lambda x: str(x).strip())
    data_frame['no_pages'] = data_frame['no_pages'].apply(lambda x: -1 if x < 0 else x)
    data_frame['no_pages'] = data_frame['no_pages'].apply(lambda x: -1 if x > 5000 else x)
    return data_frame

#Transforms data to a more readable format and removes errors
def transform_data(data_frame):
    data_frame['category'] = data_frame['category'].apply(lambda x: ast.literal_eval(x)[2] if len(ast.literal_eval(x)) > 2 else ast.literal_eval(x)[0])
    data_frame['category'] = data_frame['category'].apply(lambda x: 'unknown' if '<a' in x else x)
    data_frame['category'] = data_frame['category'].apply(lambda x: str(x).replace('&amp;', '&'))
    #data_frame['rank'] = data_frame['rank'].apply(
    #    lambda rank_string: int(rank_string.split(' ')[0].replace(',', '')) if rank_string else np.nan)
    data_frame['brand'] = data_frame['brand'].apply(lambda x: str(x).replace('Visit Amazon\'s ', ''))
    data_frame['brand'] = data_frame['brand'].apply(lambda x: str(x).replace(' Page', ''))
    data_frame['brand'] = data_frame['brand'].apply(lambda x: 'unknown' if x == 'nan' else x)



    data_frame = transform_details(data_frame)
    data_frame = reorganize_data(data_frame)
    data_frame = trim_data(data_frame)
    return data_frame


def drop_unnecessary_columns(data_frame):
    data_frame = data_frame.drop(['tech1', 'tech2',
                                  'fit', 'also_buy', 'imageURL', 'feature',
                                   'also_view', 'main_cat',
                                  'similar_item', 'date', 'price_x', 'imageURLHighRes'], axis=1)
    # data_frame = data_frame[data_frame['title'].astype(bool)]

    return data_frame

# Drops rowns with importante missing information
def drop_bad_rows(data_frame):
    data_frame['title'].replace('', np.nan, inplace=True)
    data_frame.dropna(subset=['title'], inplace=True)
    return data_frame


def get_path():
    data_set = "raw_metadata.csv"
    directory = "../datasets"
    # path = os.path.join(directory, data_set)
    # if not os.path.exists(path):
    #   print("Error:" + path + " not found")
    #  exit(1)
    # return path, directory
    return directory + "/" + data_set, directory


def drop_duplicates(data_frame):
    return data_frame.drop_duplicates(subset=['asin'])


def main():
    path, directory = get_path()
    print("READING FILE FROM " + path)

    df = pd.read_csv(path)

    df = parse_through_data(df)

    notvals = functools.reduce(operator.add, [df[c].isna().sum() for c in df.columns])
    print("Number of NaN values: " + str(notvals))

    df.to_csv(os.path.join(directory, "refined_metadata.csv"), index=False)
    return df


# %%
if __name__ == "__main__":
    main()
