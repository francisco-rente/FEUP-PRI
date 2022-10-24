import ast
import csv
import os
import pandas as pd


def read_json():
    data_set = "Kindle_Store_5.json"
    directory = "../../datasets"
    path = os.path.join(directory, data_set)
    df = pd.read_json(path, lines=True)  # read dataset
    return df


def save_to_csv(df):
    print("Saving cleaned dataset")

    # check if directory exists
    directory = "../../datasets/cleaned_data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv('../../datasets/cleaned_data/cleaned_Kindle_Reviews.csv', sep=";", index=False,
              escapechar='|')  # save to csv


def tranform_helpful(df):
    # transform helpful column to percentage
    print(df.dtypes)
    df['helpful_ratio'] = df['helpful'].apply(
        lambda x: float(x[0]) / x[1] if x[1] != 0 else 0)
    df['visualization'] = df['helpful'].apply(lambda x: x[1])
    df = df.drop(columns=['helpful'])

    return df


def clean_reviews(df):
    # df.isna().any() use this to check if any variables are Na

    df = df.fillna("Unnamed Reviewer")  # fill the single Na in reviewer name

    len_before = len(df.index)
    new_df = df.loc[df.astype(str).drop_duplicates().index]  # complicated code because of "helpful" being a list
    len_now = len(new_df.index)
    print("Removed duplicated lines") if len_now != len_before else print("Found no duplicated lines")

    new_df = tranform_helpful(new_df)  # transform helpful column to percentage

    return new_df


def main():
    print("Starting cleaning Reviews dataset")

    df = read_json()
    new_df = clean_reviews(df)
    save_to_csv(new_df)

    print("Finished cleaning Reviews dataset")


if __name__ == "__main__":
    main()
