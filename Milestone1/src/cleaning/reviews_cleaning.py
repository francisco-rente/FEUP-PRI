import ast
import csv
import os
import pandas as pd


def read_csv():
    data_set = "raw_reviews.csv"
    directory = "./datasets/merged_data/"
    path = os.path.join(directory, data_set)
    df = pd.read_csv(path)  # read dataset
    return df


def save_to_csv(df):
    print("Saving cleaned dataset")

    # check if directory exists
    directory = "./datasets/cleaned_data/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv('./datasets/cleaned_data/refined_reviews.csv',index=False)  # save to csv


def tranform_helpful(df):
    # transform helpful column to percentage
    print(df.dtypes)
    df['helpful_ratio'] = df['helpful'].apply(
        lambda x: float(ast.literal_eval(x)[0]) / (ast.literal_eval(x))[1] if (ast.literal_eval(x))[1] != 0 else 0)
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


def create_reviewer_csv(df):
    # create a csv file with all the unique reviewers
    df2 = df[['reviewerID','reviewerName']]
    df2 = df2.drop_duplicates()
    
    df2.to_csv('./datasets/cleaned_data/refined_reviewers.csv', sep=";", index=False,
              escapechar='|')  # save to csv
    
    df = df.drop(columns=['reviewerName'])
    
    return 
    
    

def main():
    print("Starting cleaning Reviews dataset")
    df = read_csv()
    df = clean_reviews(df)
    save_to_csv(df)

    print("Finished cleaning Reviews dataset")


if __name__ == "__main__":
    main()
