import pandas as pd
import matplotlib.pyplot as plt

def main():

    directory = "../../documentation/graphs/reviews"

    # Date histogram code
    df = pd.read_csv('../../datasets/cleaned_data/cleaned_Kindle_Reviews.csv', sep=";", escapechar='|')
    df_dates = df.copy()
    # df_dates = pd.to_datetime(df['unixReviewTime'],unit='s')
    df_dates['unixReviewTime'] = pd.to_datetime(df_dates['unixReviewTime'], unit='s')
    df_dates['unixReviewTime'] = df_dates['unixReviewTime'].dt.year

    # year of review ordered for graph
    graph = df_dates["unixReviewTime"].value_counts().sort_index()

    # year of review graph (histogram kinda)
    ax = graph.plot(kind='bar', title="Review number through the years", y='freq', x='Years')
    ax.set_xlabel("Year")
    ax.set_ylabel("Frequency")
    plt.savefig(directory + '/' + "review_date.png") # TODO: use fig1 = plt.gcf() plt.show() plt.draw(), instead
    plt.show()

    # overall graph stuff
    overall_graph = df["overall"].value_counts().sort_index()

    overall_plot = overall_graph.plot(kind='bar', title="Overall", y='freq', x='Years')
    overall_plot.set_ylabel("Frequency")
    overall_plot.set_xlabel("Review Grade")
    plt.savefig(directory + '/' + "overall_review_plot.png")
    plt.show()

    overal_mean = df["overall"].mean()  # mean of overall of reviews
    print("average review grade:", overal_mean)

    # text size graph
    df["reviewText_size"] = df["reviewText"].str.len()
    word_number_plot = df["reviewText_size"].value_counts().sort_index().plot()
    word_number_plot.set_xlabel("Review text word count")
    plt.savefig(directory + '/' + "text_size_plot.png")
    plt.show()


# check average of text size
    mean = df["reviewText_size"].mean()
    print("average review text word count: ", mean)


if __name__ == "__main__":
    main()
