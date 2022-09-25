import os
import pandas as pd
import datetime



def parse_through_data(data_frame):
    data_frame['category'] = data_frame['category'].apply(lambda x: x[2])
    data_frame['rank'] = data_frame['rank'].apply(lambda rank_string: int(rank_string.split(' ')[0].replace(',', '')))
    data_frame['brand'] = data_frame['brand'].apply(lambda x: x.replace('Visit Amazon\'s ', ''))
    data_frame['File Size(KB)'] = data_frame['details'].apply(lambda x: float(x['File Size:'].split(' ')[0]))
    data_frame['Print Length'] = data_frame['details'].apply(lambda x: int(x['Print Length:'].split(' ')[0]))
    data_frame['Publisher'] = data_frame['details'].apply(lambda x: x['Publisher:'])
    data_frame['Publication Date'] = data_frame['details'].apply(
        lambda x: datetime.datetime.strptime(x['Publication Date:'], '%B %d, %Y').date())

    data_frame['Language'] = data_frame['details'].apply(lambda x: x['Language:'])
    # not all objects have Page Numbers Source ISBN

    # count how many objects have Page Numbers Source ISBN: in details
    # count = df['details'].apply(lambda x: 'Page Numbers Source ISBN:' in x).sum()
    # data_frame['ISBN'] = data_frame['details'].apply(lambda x: x['Page Numbers Source ISBN:'])
    # TODO: remove all ISBN with letters?
    # TODO: get name ISBN with google's api? https://developers.google.com/books/docs/v1/using
    # DOUBT: are the prices important? 


    data_frame = data_frame.drop(['details'], axis=1)

    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]

    return data_frame


if __name__ == "__main__":
    data_set = "meta_Kindle_Store.json"
    directory = "../datasets"
    path = os.path.join(directory, data_set)

    if not os.path.exists(path):
        print("Error:" + path + " not found")
        exit(1)

    df = pd.read_json(path, lines=True)
    df = df.iloc[:10]
    # df = df.drop_duplicates(subset=['asin'])
    df = df.drop(['description',
                  'tech1', 'tech2',
                  'fit', 'title', 'also_buy',
                  'feature', 'also_view', 'main_cat',
                  'similar_item', 'imageURL', 'date', 'price', 'imageURLHighRes'], axis=1)

    df = parse_through_data(df)
    print(df.head())
    df.to_csv(os.path.join(directory, "meta_Kindle_Store.csv"), index=False)

#%%
