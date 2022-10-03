import functools
import operator
import pandas as pd
import datetime as datetime


# TODO: Check inplace vs = mechanism

# {"overall": 3.0, "vote": "3", "verified": false,
#  "reviewTime": "11 3, 2006", "reviewerID": "A3DPAR2PWB9BT8",
#  "asin": "1423600150", "style": {"Format:": " Hardcover"},
#  "reviewerName": "JJSS", "reviewText": "I admire the SF School of Cooking, but was disappointed in this cookbook.",
#  "summary": "Ok cookbook", "unixReviewTime": 1162512000}


def drop_unnecessary_columns(data_frame):
    return data_frame.drop(['vote', 'verified', 'reviewerID', 'style', 'unixReviewTime'], axis=1)


def reorganize_data(data_frame):
    return data_frame[['asin', 'overall', 'reviewerName', 'unixReviewTime', 'summary', 'reviewText']]


def transform_data(data_frame):
    data_frame['reviewTime'] = data_frame['unixReviewTime'].apply(
        lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
    return data_frame


def parse_through_data(data_frame):
    data_frame = drop_unnecessary_columns(data_frame)
    data_frame = transform_data(data_frame)
    data_frame = reorganize_data(data_frame)
    return data_frame


def get_path():
    data_set = "Kindle_Store.json"
    directory = "../datasets"
    # path = os.path.join(directory, data_set)
    # if not os.path.exists(path):
    #   print("Error:" + path + " not found")
    #  exit(1)
    # return path, directory
    return directory + "/" + data_set, directory


def main():
    path, directory = get_path()
    print("READING FILE FROM " + path)

    df = pd.read_json(path, lines=True)
    df = df.iloc[:4000]

    # df = parse_through_data(df)

    print(df.head())
    # notvals = functools.reduce(operator.add, [df[c].isna().sum() for c in df.columns])
    # print("Number of NaN values: " + str(notvals))

    # df.to_csv(os.path.join(directory, "meta_Kindle_Store.csv"), index=False)
    return df


# %%
if __name__ == "__main__":
    main()
