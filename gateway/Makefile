VERSION = v0.1.0
REPO    = kemppo/apps:gateway

gateway-build:
	docker build . --rm \
		-t $(REPO)-$(VERSION) \
		-f Dockerfile

gateway-push:
	docker push $(REPO)-$(VERSION)

gateway-push-latest:
	docker tag $(REPO)-$(VERSION) $(REPO)-latest && \
	docker push $(REPO)-latest
