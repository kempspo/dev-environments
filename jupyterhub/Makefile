VERSION  = 0.1.3
JH_NAME = jupyterhub
JH_REPO = kemppo/apps:$(JH_NAME)-$(VERSION)

docker-build:
	docker build . --rm -t $(JH_REPO)

docker-push:
	docker push $(JH_REPO)

docker-run:
	docker run -p 443:443 --rm -d --name $(JH_NAME) $(JH_REPO)

docker-bash:
	docker run -it --rm --name $(JH_NAME) $(JH_REPO) bash

docker-stop:
	docker stop $(JH_NAME)