VERSION = v1.0
REPO    = kemppo/apps:rstudio

docker-pull-latest:
	docker pull $(REPO)-latest

docker-build:
	docker build --cache-from=$(REPO)-latest -t $(REPO)-$(VERSION) .

docker-push:
	docker push $(REPO)-$(VERSION)

docker-push-latest:
	docker tag $(REPO)-$(VERSION) $(REPO)-latest && \
	docker push $(REPO)-latest
