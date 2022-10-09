# Script in charge of characterizing metadata dataset
import pandas as pd
import matplotlib.pyplot as plt


img_dir = "../../documentation/graphs/metadata"

# TODO: font size

def print_metadata_info(df):
    print("No of rows in metadata: " + str(df.shape[0]) + " and no of columns: " + str(df.shape[1]))
    print(df.describe(include='all'))
    print(df.info())
    return


def category_distribution(df):
    df['category'].value_counts().plot(kind='bar', title="Distribution of the categories", y='freq', x='category', figsize=(20, 10), fontsize=12)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(img_dir + "/category_distribution.png")
    plt.show()
    return


def brand_distribution(df):
    # Bar plot of the distribution of the top 100 brands
    df['brand'].value_counts().head(15).plot(kind='bar', title="Distribution of the top 15 brands", y='freq', x='brand')
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(img_dir + "/brand_distribution.png")
    plt.show()
    return


def category_pages_distribution(df):
    df['no_pages'].groupby(df['category']).mean().plot(kind='bar', title="Average number of pages per category",
                                                       y='no_pages', x='category')
    plt.ylabel("Average number of pages")
    plt.tight_layout()
    plt.savefig(img_dir + "/category_pages_distribution.png")
    plt.show()
    return


def category_price_distribution(df):
    df['price'].groupby(df['category']).median().plot(kind='bar', title="Price per category", y='price ($)', x='category')
    plt.ylabel("Median price ($)")
    plt.tight_layout()
    plt.savefig(img_dir + "/category_price_distribution.png")
    plt.show()
    return


def brand_price_median(df):
    df['price'].groupby(df['brand']).median().head(15).plot(kind='bar', title="Price per author (Median)", y='price ($)',
                                                   x='author')
    plt.ylabel("Median price ($)")
    plt.tight_layout()
    plt.savefig(img_dir + "/brand_price_median.png")
    plt.show()
    return


def average_title_size_category(df):
    new_df = df.copy()
    new_df['title_size'] = new_df['title'].str.len()
    new_df['title_size'].groupby(new_df['category']).mean().plot(kind='bar', title="Average title size per category",
                                                                 y='title_size', x='category')
    plt.ylabel("Average title size")
    plt.tight_layout()
    plt.savefig(img_dir + "/average_title_size_category.png")
    plt.show()
    return


def description_size_category_distribution(df):
    new_df = df.copy()
    new_df['description_size'] = new_df['description'].str.len()
    new_df['description_size'].groupby(new_df['category']).mean().plot(kind='bar', title="Average description size per category",
                                                                 y='description_size', x='category')
    plt.tight_layout()
    plt.savefig(img_dir + "/description_size_category_distribution.png")
    plt.show()
    return


def description_word_play(df):
    pass


def graphs(df):
    brand_distribution(df)
    brand_price_median(df)

    category_distribution(df)
    category_pages_distribution(df)
    category_price_distribution(df)
    average_title_size_category(df)
    description_size_category_distribution(df)

    return


def statistics(df):
    print_metadata_info(df)
    description_word_play(df)
    return


def main():
    df = read_dataset()

    graphs(df)
    statistics(df)

    return 0


def read_dataset():
    df = pd.read_csv("../../datasets/cleaned_data/refined_metadata.csv")
    return df


if __name__ == "__main__":
    main()
