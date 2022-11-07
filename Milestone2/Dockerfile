FROM solr:8.10

# Copy data to the container
COPY /data/solr_data.json /data/solr_data.json
# Copy the schema to the container

#Copy the startup script
COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
