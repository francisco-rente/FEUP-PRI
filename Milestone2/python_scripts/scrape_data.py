import pandas as pd 
from bs4 import BeautifulSoup as bs
import requests as requests

def read_df(): 
    return pd.read_json('../data/solr_metadata.json', lines=True)


def main(): 
    df = read_df()
    print(len(df))
    print("Number of NaN values in description column: ", df[df["description"] == "no description"].shape[0] / len(df))
    
    df_missing = df[df["description"] == "no description"]
    df_missing = df_missing[["id","description"]]

    print(df.head())
    url = "https://www.amazon.com/exec/obidos/ASIN/"
    url = "http://www.amazon.com/exec/obidos/tg/detail/-/"
    for i in range(10): 
        fetch_ulr = url + df_missing["id"].iloc[i] + "/"
        print(fetch_ulr)
        page = requests.get(fetch_ulr)
        print(page.content)
        # soup = bs(page, "lxml")
        # print(soup.title)
        # div = soup.find(id="book_description_expander")
        # print(div)
        # inner_div = soup.find(id="book_description_expander").next_sibling
        # description = " ".join([p.text for p in inner_div.find_all("p")])
        # print(description)

        

if __name__ == "__main__": 
    main()