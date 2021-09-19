# RStudio Server Docker Image
FROM rocker/geospatial:4.1.1
LABEL maintainer="Kemp Po kempspo@gmail.com"

# Linux Dependencies
RUN apt-get update && \
	apt-get install -y \
	curl \
	dumb-init \
	zsh \
	htop \
	locales \
	man \
	nano \
	git \
	procps \
	openssh-client \
	sudo \
	vim.tiny \
	lsb-release \
	gdebi-core \
	apt-utils \
	software-properties-common \
	curl \
	gnupg-agent \
	ca-certificates \
	nano \
	zsh \
	gnupg \
	apt-transport-https \
	libsodium-dev \
	nodejs \
	make \
	wget \
	xvfb \
	libssh-dev \
	nginx \
	libpoppler-cpp-dev

# Install Docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
	sudo apt-key fingerprint 0EBFCD88 && \
	sudo add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) \
	stable" && \
	apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io && \
	usermod -aG docker rstudio && usermod -aG rstudio-server rstudio

# Install kubectl
RUN apt-get update && apt-get install -y apt-transport-https && \
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list && \
  apt-get update && apt-get install -y kubectl

# Install Cloud66 Toolbelt
RUN curl -sSL https://s3.amazonaws.com/downloads.cloud66.com/cx_installation/cx_install.sh | bash

# Install Git LFS
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash && \
	apt-get update && apt-get install -y git-lfs

# Install Google Chrome (Headless Browsing)
RUN wget \
    https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    sudo apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb

# Rprofile.site
COPY Rprofile.site /usr/local/lib/R/etc/Rprofile.site

# Expose JupyterHub Port
EXPOSE 8888

# More R Packages
RUN install2.r renv

# New Entrypoint
COPY rstudio_hub.sh /cmd/rstudio_hub.sh
CMD ["/cmd/rstudio_hub.sh"]