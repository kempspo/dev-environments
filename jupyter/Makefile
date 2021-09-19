VERSION = v1.1.1
REPO    = kemppo/apps:jupyter

docker-build:
	docker build . --rm -t $(REPO)-$(VERSION)

docker-push:
	docker push $(REPO)-$(VERSION)

docker-push-latest:
	docker tag $(REPO)-$(VERSION) $(REPO)-latest && \
	docker push $(REPO)-latest
