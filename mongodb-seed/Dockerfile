FROM mongo:latest
WORKDIR /tmp
COPY ./data/events.json ./data/events.json
CMD mongoimport --host 172.16.0.2 --db conflict_db --collection events --type json  --file /tmp/data/events.json --jsonArray --drop