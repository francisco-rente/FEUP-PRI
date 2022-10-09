#Matches the dataframes and saves them on csv files

import pandas as pd


def main():
    # Read both dataframes
    print("READING METADATA JSON...")
    dfmeta = pd.read_json('../../datasets/meta_Kindle_Store_2018.json', lines=True)
    print("READING REVIEWS JSON...")
    dfreviews = pd.read_json('../datasets/reviews_Kindle_Store_2014.json', lines=True)
    print("READ ALL DATAFRAMES... READY FOR MATCHING")

    print("PRODUCTS DATAFRAME:" + str(dfmeta.shape[0]) + "," + str(dfmeta.shape[1]))
    print("UNIQUE PRODUCTS IN METADATA:" + str(dfmeta['asin'].nunique()))
    print("REVIEWS DATAFRAME:"  + str(dfreviews.shape[0]) + "," + str(dfreviews.shape[1]))
    print("UNIQUE PRODUCTS IN REVIEWS:" + str(dfreviews['asin'].nunique()))

    print("MATCHING PRODUCTS AND REVIEWS")
    dfmeta = dfmeta[dfmeta.asin.isin(dfreviews.asin)]
    dfreviews = dfreviews[dfreviews.asin.isin(dfmeta.asin)]
    print("MATCHING IS DONE. CHECKING RESULTS")

    print("PRODUCTS DATAFRAME:" + str(dfmeta.shape[0]) + "," + str(dfmeta.shape[1]))
    print("UNIQUE PRODUCTS IN METADATA:" + str(dfmeta['asin'].nunique()))
    print("REVIEWS DATAFRAME:"  + str(dfreviews.shape[0]) + "," + str(dfreviews.shape[1]))
    print("UNIQUE PRODUCTS IN REVIEWS:" + str(dfreviews['asin'].nunique()))

    print("SAVING DATAFRAMES ON CSV FILES")
    dfmeta.to_csv('../datasets/raw_unmerged_metadata.csv', index=False)
    dfreviews.to_csv('../datasets/raw_reviews.csv', index=False)

    return 0


if __name__ == "__main__":
    main()

