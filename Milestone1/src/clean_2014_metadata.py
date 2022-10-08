import ast
import json
import html
import sys
import unicodedata as ud
import pandas as pd


def clean_description(description):
    description = ud.normalize('NFKD', description).encode('ascii', 'ignore').decode('ascii')
    description = description.replace('`', "'")
    description = html.unescape(description)
    description = description.replace(u'\xa0', ' ')

    return description


def clean_metadata(metadata):
    if verbose_mode():
        print("--------------------")
        print("Cleaning metadata")

    initial_shape = metadata.shape

    metadata = metadata.drop_duplicates(subset=['asin'])

    if verbose_mode():
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " duplicate asin")

    metadata = metadata[metadata['price'] > 0]

    if verbose_mode():
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with price <= 0")

    metadata = metadata[metadata['imUrl'] != 'no reference']

    if verbose_mode():
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no reference image")

    metadata = metadata[metadata['imUrl'].str.contains('http')]

    if verbose_mode():
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no http in image url")

    metadata = metadata[metadata['description'] != 'no description']

    if verbose_mode():
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no description")

    # metadata = metadata[metadata['price'].notna()]

    metadata["description"] = metadata["description"].apply(clean_description)

    if verbose_mode():
        print("Cleaned description")

    final_shape = metadata.shape
    if verbose_mode():
        print("Removed " + str(initial_shape[0] - final_shape[0]) + " rows")

    if verbose_mode():
        print("--------------------")

    return metadata


def verbose_mode():
    return len(sys.argv) > 1 and sys.argv[1] == "-v"


def parse_metadata():
    metadata_list = []
    with open('../datasets/meta_Kindle_Store_2014.json', 'r') as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            count += 1
            # if len(sys.argv) > 1 and sys.argv[1] == "-v" and count % 10000 == 0:
            #     print("Parsed " + str(count) + " lines")
            # if count == 10000:
            #     break
            dic = ast.literal_eval(line)
            metadata_list.append({'asin': dic['asin'],
                                  'price': dic['price'] if 'price' in dic else None,
                                  'imUrl': dic['imUrl'] if 'imUrl' in dic else 'no reference',
                                  'description': dic['description'] if 'description' in dic else 'no description'})

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Metadata file contains " + str(len(metadata_list)) + " objects")

    # transform list of dictionaries into dataframe
    metadata = pd.DataFrame(metadata_list)
    return metadata


def print_final_shape(metadata):
    print("--------------------")
    print("Cleaned metadata shape: " + str(metadata.shape[0]) + " rows, " + str(metadata.shape[1]) + " columns")
    # print NA values in price
    print("Number of NA values in price: " + str(metadata['price'].isna().sum()))
    # print no of description == no description
    print("Number of description == no description: " + str((metadata['description'] == 'no description').sum()))
    # print no of imUrl == no reference
    print("Number of imUrl == no reference: " + str((metadata['imUrl'] == 'no reference').sum()))
    # print no of imUrl not containing http
    print("Number of imUrl not containing http: " + str((~metadata['imUrl'].str.contains('http')).sum()))
    print("--------------------")


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
        print("Describing metadata")
        print(metadata.describe(include='all'))

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Saving cleaned metadata to file")

    metadata.to_csv('../datasets/cleaned_2014_metadata.csv', index=False)

    # metadata = pd.read_csv('../datasets/cleaned_2014_metadata.csv')
    # if len(sys.argv) > 1 and sys.argv[1] == "-v":
    #     print(metadata.shape[0])


if __name__ == "__main__":
    main()
