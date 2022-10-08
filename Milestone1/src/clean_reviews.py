import os
import pandas as pd


def main():
    data_set = "Kindle_Store_5.json"
    directory = "../datasets"
    path = os.path.join(directory, data_set)

    df = pd.read_json(path, lines=True)  # read dataset

    # df.isna().any() use this to check if any variables are Na

    df = df.fillna("Unnamed Reviewer")  # fill the single Na in reviewer name

    len_before = len(df.index)
    new_df = df.loc[df.astype(str).drop_duplicates().index]  # complicated code because of "helpful" being a list
    len_now = len(new_df.index)

    print("Removed duplicated lines") if len_now != len_before else print("Found no duplicated lines")

    print("Saving cleaned dataset")
    new_df.to_csv('../datasets/cleaned_Kindle_Reviews.csv', index=False)  # save to csv
    print("Finished cleaning Reviews dataset")


if __name__ == "__main__":
    main()
