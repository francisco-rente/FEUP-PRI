FROM solr:8.10

# Copy data to the container
COPY /data/solr_metadata.json /data/solr_metadata.json
COPY /data/solr_reviews.json /data/solr_reviews.json
# Copy the schema to the container
COPY /schema_scripts/metadata_schema.json /schema_scripts/metadata_schema.json
COPY /schema_scripts/reviews_schema.json /schema_scripts/reviews_schema.json
#Copy the startup script
COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]