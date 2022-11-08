# Picks the datasets from the cleaned_data folder and converts them to one compact json

# Reviews file path -> data/reviews.json
# Metadata file path -> data/metadata.json

# Importing important data
import pandas as pd

# Reads the reviews and metadata file and returns both dataframes
def read_dataframes():
    reviews = pd.read_json('data/reviews.json', lines=True)
    metadata = pd.read_json('data/metadata.json', lines=True)
    
    reviews.insert(0, 'id',range(0, len(reviews)))
    

    return reviews, metadata




def main():
    
    # Reads the dataframes
    reviews, metadata = read_dataframes()
    
    # Change the dataframe to be ready to Solr    
    # Go through each metadata row and add the review to the metadata
    
    # Create an 'id' column from 'asin' column
    metadata.rename(columns={'asin': 'id'}, inplace=True)
    
    metadata.to_json('data/solr_metadata.json', orient='records', lines=True)
    reviews.to_json('data/solr_reviews.json', orient='records', lines=True)
    

    return




if __name__ == "__main__":
    main()
