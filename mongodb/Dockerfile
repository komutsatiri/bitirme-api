FROM mongo:3.2.11
WORKDIR /tmp
COPY ./data/events.json ./data/events.json
CMD mongoimport --host db --db conflict_db --collection events --type json  --file /tmp/data/events.json --jsonArray



