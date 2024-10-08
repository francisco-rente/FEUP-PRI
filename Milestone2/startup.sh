#!/bin/bash
# Pre create the core
precreate-core kindle
precreate-core sampled_kindle

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 5

cp /schema_scripts/mysynonyms.txt /var/solr/data/kindle
cp /schema_scripts/en_stopwords.txt /var/solr/data/kindle


cp /schema_scripts/mysynonyms.txt /var/solr/data/sampled_kindle
cp /schema_scripts/en_stopwords.txt /var/solr/data/sampled_kindle


curl -X POST -H 'Content-type:application/json' \
    --data-binary @/schema_scripts/kindle_schema.json \
    http://localhost:8983/solr/kindle/schema


curl -X POST -H 'Content-type:application/json' \
    --data-binary @/schema_scripts/kindle_schema.json \
    http://localhost:8983/solr/sampled_kindle/schema


curl -X POST -H 'Content-type:application/json'  -d '{
  "add-searchcomponent": {
    "name": "suggest",
    "class": "solr.SuggestComponent",
    "suggester": {
        "name": "mySuggester",
        "lookupImpl": "FuzzyLookupFactory",
        "dictionaryImpl": "DocumentDictionaryFactory",
        "field": "title",
        "suggestAnalyzerFieldType": "text_general",
        "exactMatchFirst": "true",
        "buildOnStartup": "true"
    }
  }
}' http://localhost:8983/solr/kindle/config

curl -X POST -H 'Content-type:application/json'  -d '{
  "add-requesthandler": {
    "name": "/suggest",
        "class": "solr.SearchHandler",
        "startup": "lazy",
        "defaults": {
            "suggest": true,
            "suggest.count": 20,
            "suggest.dictionary": "mySuggester"
        },
        "components": [
            "suggest"
        ]
  }
}' http://localhost:8983/solr/kindle/config

# "add-copy-field": {
#         "source": "title",
#         "dest": "title_suggest"
#     }


# Populate collection
bin/post -c kindle /data/solr_metadata.json
bin/post -c kindle /data/solr_reviews.json

# Populate sampled collection
bin/post -c sampled_kindle /data/solr_sampled_metadata.json
bin/post -c sampled_kindle /data/solr_sampled_reviews.json

# Restart in foreground mode so we can access the interface
solr restart -f
