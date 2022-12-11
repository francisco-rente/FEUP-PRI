FROM solr:8.10

# Copy data to the container
COPY /data/solr_metadata.json /data/solr_metadata.json
COPY /data/solr_reviews.json /data/solr_reviews.json


# Copy sampled data to the container
COPY /data/solr_sampled_metadata.json /data/solr_sampled_metadata.json
COPY /data/solr_sampled_reviews.json /data/solr_sampled_reviews.json


# Copy the schema to the container
COPY /schema_scripts/kindle_schema.json /schema_scripts/kindle_schema.json
# Simple Schema 
COPY /schema_scripts/analyserless_schema.json /schema_scripts/analyserless_schema.json


# Copy synonyms mysynonyms
COPY /schema_scripts/mysynonyms.txt /schema_scripts/mysynonyms.txt
# Copy stopwords
COPY /schema_scripts/en_stopwords.txt /schema_scripts/en_stopwords.txt

#Copy the startup script
COPY startup.sh /scripts/startup.sh


ENTRYPOINT ["/scripts/startup.sh"]