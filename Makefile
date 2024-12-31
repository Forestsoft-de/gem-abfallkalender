include .secrets
build:
	docker build -t read-ical .

run:
	docker run -e TODOIST_API_TOKEN=${TODOIST_API_TOKEN} -v $(shell pwd):/app read-ical

# Add more targets for other actions like pushing the image to a registry
# push:
# 	docker push your-registry/read-ical:latest