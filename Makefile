GCP_PROJECT_ID=GCP-PROJECT-NAME
DOCKER_IMAGE_NAME=twitch-api
GCR_MULTI_REGION=eu.gcr.io
GCR_REGION=europe-west1

# run api locally
run_api:
	uvicorn api:app --reload

# for apple silicon
build_m1_local:
	docker build -t ${DOCKER_IMAGE_NAME} .

run_m1_local:
	docker run -e PORT=8000 -p 8080:8000 ${DOCKER_IMAGE_NAME}

build_m1_prod:
	docker build --platform linux/amd64 -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} .

# for other machines
build_image:
	docker build -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} .

run_image:
	docker run -e PORT=8000 -p 8080:8000 ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

# check conf
check_auth:
	gcloud auth list

check_conf:
	gcloud config list

conf_docker_gcloud:
	gcloud auth configure-docker

# put in production
push_image:
	docker push ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

deploy_image:
	gcloud run deploy --image ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} --platform managed --region ${GCR_REGION}
