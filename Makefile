start_server:
	uvicorn tumor_class.api.api:app --host localhost --reload

start_hello:
	python -c 'from tumor_class.api.hello import hello_world()'

docker_build:
	docker build . -t eu.gcr.io/$GCP_PROJECT/$IMAGE

docker_push:
	docker push eu.gcr.io/$GCP_PROJECT/$IMAGE
