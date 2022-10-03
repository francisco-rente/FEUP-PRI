import os

import numpy as np
import pandas as pd
import datetime
import operator, functools

def parse_through_data(data_frame):
    df = drop_unnecessary_columns(data_frame)
    df = drop_duplicates(df)
    df = transform_data(df)
    return df


def transform_isbn(data_frame):
    # data_frame[data_frame['details'].apply(lambda x: 'Page Numbers Source ISBN:' in x)]
    data_frame['ISBN'] = data_frame['details'].apply(
        lambda x: x['Page Numbers Source ISBN:'].replace('ISBN-10: ', '')
        if 'Page Numbers Source ISBN:' in x else np.nan)
    return data_frame


def transform_details(data_frame):
    data_frame['File Size(KB)'] = data_frame['details']. \
        apply(lambda x: float(x['File Size:'].split(' ')[0]) if 'File Size:' in x else np.nan)
    data_frame['Print Length'] = data_frame['details']. \
        apply(lambda x: int(x['Print Length:'].split(' ')[0]) if 'Print Length:' in x else np.nan)
    data_frame['Publisher'] = data_frame['details']. \
        apply(lambda x: x['Publisher:'].split(';')[0] if 'Publisher:' in x else np.nan)
    data_frame['Publication Date'] = data_frame['details'].apply(
        lambda x: datetime.datetime.strptime(x['Publication Date:'], '%B %d, %Y').date()
        if 'Publication Date:' in x else np.nan)
    data_frame['Language'] = data_frame['details']. \
        apply(lambda x: x['Language:'] if 'Language:' in x else np.nan)
    data_frame = transform_isbn(data_frame)
    data_frame = data_frame.drop(['details'], axis=1)
    return data_frame


def reorganize_data(data_frame):
    # cols = data_frame.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    # data_frame = data_frame[cols]
    return data_frame[['asin', 'title', 'brand', 'rank', 'category', 'File Size(KB)',
                       'Print Length', 'Publisher', 'Publication Date', 'Language', 'ISBN']]


def transform_data(data_frame):
    data_frame['category'] = data_frame['category'].apply(lambda x: x[2] if len(x) > 2 else x[0])
    data_frame['rank'] = data_frame['rank'].apply(
        lambda rank_string: int(rank_string.split(' ')[0].replace(',', '')) if rank_string else np.nan)
    data_frame['brand'] = data_frame['brand'].apply(lambda x: x.replace('Visit Amazon\'s ', ''))
    data_frame = transform_details(data_frame)
    data_frame = reorganize_data(data_frame)
    return data_frame


def drop_unnecessary_columns(data_frame):
    data_frame = data_frame.drop(['description',
                                  'tech1', 'tech2',
                                  'fit', 'also_buy',
                                  'feature', 'also_view', 'main_cat',
                                  'similar_item', 'imageURL', 'date', 'price', 'imageURLHighRes'], axis=1)
    # data_frame = data_frame[data_frame['title'].astype(bool)]
    data_frame['title'].replace('', np.nan, inplace=True)
    data_frame.dropna(subset=['title'], inplace=True)
    return data_frame


def get_path():
    data_set = "meta_Kindle_Store.json"
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

    df = pd.read_json(path, lines=True)
    df = df.iloc[:4000]

    df = parse_through_data(df)

    print(df.head())
    notvals = functools.reduce(operator.add, [df[c].isna().sum() for c in df.columns])
    print("Number of NaN values: " + str(notvals))

    # df.to_csv(os.path.join(directory, "meta_Kindle_Store.csv"), index=False)
    return df


# %%
if __name__ == "__main__":
    main()
