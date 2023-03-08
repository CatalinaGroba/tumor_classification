start_server:
	uvicorn tumor_class.api.api:app --host localhost

start_hello:
	python -c 'from tumor_class.api.hello import hello_world()'
