FROM codercom/code-server:3.2.0
LABEL maintainer="Kemp Po kempspo@gmail.com"

USER root

# Linux Dependencies
RUN apt-get update && apt-get -y install \
  gdebi-core \
  apt-utils \
  curl \
  nano \
  software-properties-common \
  zsh \
  gnupg2 \
  nginx \
  build-essential

RUN apt-get update && \
  apt-get install -y python3-pip

# Install Docker & ZSH
USER root
RUN sudo apt-get update && sudo apt-get install -y lsb-release software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) \
    stable" && \
    apt-get update && apt-get install -y docker-ce=19.03.8 docker-ce-cli containerd.io

# Install kubectl
RUN apt-get update && apt-get install -y apt-transport-https && \
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list && \
  apt-get update && apt-get install -y kubectl

# Install Cloud66 Toolbelt
RUN curl -sSL https://s3.amazonaws.com/downloads.cloud66.com/cx_installation/cx_install.sh | bash

# Expose JupyterHub Port
EXPOSE 8888

# Switch back to coder user
USER coder

# New Entrypoint
COPY vscode_hub.sh /cmd/vscode_hub.sh
ENTRYPOINT ["/cmd/vscode_hub.sh"]
