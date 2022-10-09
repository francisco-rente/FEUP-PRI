import ast
import json
import html
import sys
import unicodedata as ud
import re

import pandas as pd


def clean_description(description):
    description = ud.normalize('NFKD', description).encode('ascii', 'ignore').decode('ascii')
    description = description.replace('`', "'")
    description = description.replace('\'\'', "'")
    description = html.unescape(description)
    description = description.replace(u'\xa0', ' ')
    # remove LS and PS
    description = description.replace(u'\u2028', ' ')
    description = description.replace(u'\u2029', ' ')

    return description


def clean_metadata(metadata):
    if verbose_mode():
        print("--------------------")
        print("Cleaning metadata")

    initial_shape = metadata.shape

    metadata = metadata.drop_duplicates(subset=['asin'])

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " duplicate asin")

    metadata = metadata[metadata['price'] > 0]

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with price <= 0")

    metadata = metadata[metadata['imgUrl'] != 'no reference']

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no reference image")

    metadata = metadata[metadata['imgUrl'].str.contains('http')]

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no http in image url")

    metadata = metadata[metadata['description'] != 'no description']

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with no description")

    # metadata = metadata[metadata['price'].notna()]

    metadata["description"] = metadata["description"].apply(clean_description)

    if verbose_mode():
        print("Cleaned description")

    rex = re.compile(r'<href.*?>(.*?)</href>|<a.*?>(.*?)</a>|<ul.*?>(.*?)</ul>', re.S | re.M) # rex.match(data)
    metadata = metadata[metadata['description'].apply(lambda x: rex.match(x) is None)]

    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
        print("Removed " + str(initial_shape[0] - metadata.shape[0]) + " rows with html tags in description")

    final_shape = metadata.shape
    if verbose_mode() and initial_shape[0] != metadata.shape[0]:
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

            # if len(sys.argv) > 1 and sys.argv[1] == "-v" and count % 10000 == 0:
            #     print("Parsed " + str(count) + " lines")

            dic = ast.literal_eval(line)
            metadata_list.append({'asin': dic['asin'],
                                  'price': dic['price'] if 'price' in dic else None,
                                  'imgUrl': dic['imUrl'] if 'imUrl' in dic else 'no reference',
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
    # print no of imgUrl == no reference
    print("Number of imgUrl == no reference: " + str((metadata['imgUrl'] == 'no reference').sum()))
    # print no of imgUrl not containing http
    print("Number of imgUrl not containing http: " + str((~metadata['imgUrl'].str.contains('http')).sum()))
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