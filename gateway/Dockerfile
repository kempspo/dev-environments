# VS Code Gateway
FROM quay.io/oauth2-proxy/oauth2-proxy:v7.1.3
LABEL maintainer="Kemp Po kempspo@gmail.com"

USER root

# Copy Authenticated Email List
RUN mkdir -p /src
COPY authenticated_emails.cfg /src/authenticated_emails.cfg
USER 2000:2000
