#!/bin/bash

# Pre create the core
precreate-core books
precreate-core reviews

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/schema_scripts/metadata_schema.json \
    http://localhost:8983/solr/books/schema

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/schema_scripts/reviews_schema.json \
    http://localhost:8983/solr/reviews/schema

# Populate collection
bin/post -c books /data/solr_metadata.json
bin/post -c reviews /data/solr_reviews.json

# Restart in foreground mode so we can access the interface
solr restart -f
