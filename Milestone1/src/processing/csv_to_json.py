import os
import pandas as pd

    
def main():
    if(os.path.exists("datasets/cleaned_data/refined_metadata.csv")):
        df = pd.read_csv("datasets/cleaned_data/refined_metadata.csv")
        df.to_json("datasets/cleaned_data/refined_metadata.json", orient="records", lines=True)
        df.to_json("../Milestone2/data/metadata.json", orient="records", lines=True)
        os.remove("datasets/cleaned_data/refined_metadata.csv")
        
    if(os.path.exists("datasets/cleaned_data/refined_reviews.csv")):
        df = pd.read_csv("datasets/cleaned_data/refined_reviews.csv")
        df.to_json("datasets/cleaned_data/refined_reviews.json", orient='records', lines=True)
        df.to_json("../Milestone2/data/reviews.json", orient='records', lines=True)
        os.remove("datasets/cleaned_data/refined_reviews.csv")
        
    
    return



if __name__ == "__main__":
    main()