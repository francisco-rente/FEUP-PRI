# Merges the two dataframes into one
# Use this if I can get metadata from 2014 working
# Not using

import pandas as pd


def merge_metadata(df1, df2):
    return pd.merge(df1, df2, how='left', on='asin')


def main():
    # Read both dataframes
    df2018 = pd.read_csv('../datasets/raw_unmerged_metadata.csv')
    df2014 = pd.read_csv('../../datasets/cleaned_2014_metadata.csv')

    df_metadata = merge_metadata(df2018, df2014)
    df_metadata.to_csv('../datasets/raw_metadata.csv', index=False)
    return 0


if __name__ == "__main__":
    main()
