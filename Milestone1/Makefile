DATASETS_DIR = "../datasets"
2014_META_DATA_FILE = "meta_Kindle_Store_2014.json"
2018_META_DATA_FILE = "meta_Kindle_Store_2018.json"
REVIEWS_FILE = "reviews_Kindle_Store_2014.json"


# general steps

# A BIT CONFUSING RIGHT NOW

# metadata_2014_cleaning
# takes meta_Kindle_Store_2014.json -> cleaned_2014_metadata.csv

# reviews_cleaning
# takes Kindle_Store_5.json -> cleaned_reviews.csv

# metadata_2018_cleaning
# takes meta_Kindle_Store_2018.json -> raw_metadata.csv

# data_matching
# takes reviews_Kindle_Store_2014.csv (HOW?), meta_Kindle_Store_2018.json -> raw_unmerged_metadata.csv and raw_reviews.csv

# metadata_merge
# takes raw_unmerged_metadata.csv, cleaned_2014_metadata.csv -> raw_metadata.csv

# FOR IT TO BE LINEAR, THE JSON READ (BECAUSE OF THE DESCRIPTION) in 2014 should be done separately.
# data_match should be done after the read, maybe with a clean 2014 json?


help:
	@echo "MAKE INSTRUCTIONS"
	@echo "Ensure a virtual environment is activated"
	@echo "check_datasets: check if the datasets are available"
	@echo "match_datasets: match the datasets"
	@echo "clean_data: clean both datasets"
	@echo "clean_reviews: cleans reviews dataset"
	@echo "clean_metadata: cleans metadata dataset"
	@echo "process_data: process the datasets"
	@echo "characterize_reviews: characterize the reviews dataset"
	@echo "characterize_metadata: characterize the metadata dataset"

all: check_datasets match_datasets clean_data characterize_data csv_to_json 

check_datasets:
	# verify that the datasets directory exists
	[ -d $(DATASETS_DIR) ] || (echo "ERROR: $(DATASETS_DIR) does not exist"; exit 1)
	# verify that the 2014 meta data file exists
	[ -f $(DATASETS_DIR)/$(2014_META_DATA_FILE) ] || (echo "ERROR: $(DATASETS_DIR)/$(2014_META_DATA_FILE) does not exist"; exit 1)
	# verify that the 2018 meta data file exists
	[ -f $(DATASETS_DIR)/$(2018_META_DATA_FILE) ] || (echo "ERROR: $(DATASETS_DIR)/$(2018_META_DATA_FILE) does not exist"; exit 1)
	# verify that the reviews file exists
	[ -f $(DATASETS_DIR)/$(REVIEWS_FILE) ] || (echo "ERROR: $(DATASETS_DIR)/$(REVIEWS_FILE) does not exist"; exit 1)


match_datasets: check_datasets
	python3 src/processing/match_datasets.py
	# check if the matched datasets file exists

# Converts 2014 metadata to readable csv
# Cleans 2014 metadata
# Merges 2018 metadata with 2014 metadata
# Creates a raw metadata file
merge_cleaning:
	python3 src/processing/metadata_2014_converison.py
	python3 src/processing/metadata_merge.py


clean_data: clean_reviews clean_metadata

characterize_data: characterize_reviews characterize_metadata
	python3 characterize_data.py

# Cleans the reviews metadata and creates the refined_reviews.csv
# Also creates the refined_reviewers.csv
clean_reviews:
	python3 src/cleaning/reviews
	# check if the clean dataset file exists

clean_metadata:
	python3 src/cleaning/metadata_cleaning.py
	# check if the clean dataset file exists

characterize_metadata:
	python3 characterize_metadata.py
	# check if the metadata characterization file exists

characterize_reviews:
	python3 characterize_reviews.py
	# check if the reviews characterization file exists


csv_to_json:
	python3 src/processing/csv_to_json.py