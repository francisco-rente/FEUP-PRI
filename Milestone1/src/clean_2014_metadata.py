import ast
import json
import sys

import pandas as pd


def clean_metadata(metadata):
    metadata = metadata[metadata['price'] > 0]
    metadata = metadata[metadata['imUrl'] != 'no reference']
    metadata = metadata[metadata['imUrl'].str.contains('http')]
    metadata = metadata[metadata['description'] != 'no description']
    metadata['description'] = metadata['description'].str.replace('&#x22;', '"')
    return metadata


def parse_metadata():
    metadata_list = []
    with open('../datasets/meta_Kindle_Store_2014.json', 'r') as f:
        lines = f.readlines()
        for line in lines:
            dic = ast.literal_eval(line)
            metadata_list.append({'asin': dic['asin'],
                                  'price': dic['price'] if 'price' in dic else None,
                                  'imUrl': dic['imUrl'] if 'imUrl' in dic else 'no reference',
                                  'description': dic['description'] if 'description' in dic else 'no description'})

    print("Metadata file contains " + str(len(metadata_list)) + " objects")
    df = pd.DataFrame(columns=['asin', 'price', 'imUrl', 'description'])

    for i in range(len(metadata_list)):
        df = pd.concat([df, pd.DataFrame([metadata_list[i]])],
                       ignore_index=True)

    return df


def print_final_shape(metadata):
    print("Cleaned metadata shape: " + str(metadata.shape[0]) + " rows, " + str(metadata.shape[1]) + " columns")
    # print NA values in price
    print("Number of NA values in price: " + str(metadata['price'].isna().sum()))
    # print no of description == no description
    print("Number of description == no description: " + str((metadata['description'] == 'no description').sum()))
    # print no of imUrl == no reference
    print("Number of imUrl == no reference: " + str((metadata['imUrl'] == 'no reference').sum()))
    # print no of imUrl not containing http
    print("Number of imUrl not containing http: " + str((~metadata['imUrl'].str.contains('http')).sum()))



def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Reading metadata from file")

    metadata = parse_metadata()

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Parsed metadata")

    metadata = clean_metadata(metadata)

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print_final_shape(metadata)

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Saving cleaned metadata to file")

    metadata.to_csv('../datasets/cleaned_2014_metadata.csv', index=False)


if __name__ == "__main__":
    main()
