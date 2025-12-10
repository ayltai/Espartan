DOCKER_OWNER = ayltai
DOCKER_REPO  = geekylifehacks
PRODUCT_NAME = espartan-master
VERSION      = 0.1.0

deploy: prune build publish

build:
	DOCKER_BUILDKIT=1 docker build --no-cache -t ${DOCKER_OWNER}/${DOCKER_REPO}:${PRODUCT_NAME}-${VERSION} -f backend/Dockerfile .

docker:
	docker run -p 8000:8000 ${DOCKER_OWNER}/${DOCKER_REPO}:${PRODUCT_NAME}-${VERSION}

publish:
	docker push ${DOCKER_OWNER}/${DOCKER_REPO}:${PRODUCT_NAME}-${VERSION}

prune:
	docker image remove ${DOCKER_OWNER}/${DOCKER_REPO}:${PRODUCT_NAME}-${VERSION} || true
	docker system prune -f
