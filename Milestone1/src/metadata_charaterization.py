# Script in charge of caraterizing metadata dataset

import pandas as pd
import matplotlib.pyplot as plt


def print_metadata_info(df):
    print(df.columns)
    print(df.dtypes)
    print(df.describe(include='all'))
    print(df.info())
    return 

def category_distribution(df):
    df['category'].value_counts().plot(kind='bar')
    plt.show()
    return

def brand_distribution(df):
    #Bar plot of the distribution of the top 100 brands
    df['brand'].value_counts().head(15).plot(kind='bar')
    plt.show()


    return



def main():
    df = pd.read_csv("../datasets/refined_metadata.csv")
    #print_metadata_info(df)
    #category_distribution(df)
    brand_distribution(df)


    return 0 


if __name__ == "__main__":
    main()