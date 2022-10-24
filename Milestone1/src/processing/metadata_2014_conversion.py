import ast
import sys

import pandas as pd

def parse_metadata():
    metadata_list = []
    with open('./datasets/meta_Kindle_Store_2014.json', 'r') as f:
        lines = f.readlines()
        for line in lines:
            dic = ast.literal_eval(line)
            metadata_list.append({'asin': dic['asin'],
                                  'price': dic['price'] if 'price' in dic else None,
                                  'imgUrl': dic['imUrl'] if 'imUrl' in dic else 'no reference',
                                  'description': dic['description'] if 'description' in dic else 'no description'})

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print("Metadata file contains " + str(len(metadata_list)) + " objects")

    metadata = pd.DataFrame(metadata_list)
    return metadata


def save_to_file(metadata):
    metadata.to_csv('./datasets/cleaned_data/valid_metadata_2014.csv', index=False)


def main():
    print("Converting 2014 metadata to a valid csv file")
    metadata = parse_metadata()
    save_to_file(metadata)
    print("END of conversion")
    return 0


if __name__ == "__main__":
    main()