VERSION = v1.3.0
REPO    = kemppo/apps:vscode

docker-build:
	docker build . --rm -t $(REPO)-$(VERSION)

docker-push:
	docker push $(REPO)-$(VERSION)

docker-push-latest:
	docker tag $(REPO)-$(VERSION) $(REPO)-latest && \
	docker push $(REPO)-latest
