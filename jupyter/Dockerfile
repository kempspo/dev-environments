FROM jupyter/datascience-notebook:4cdbc9cdb7d1

# Switch to root and install system dependencies
USER root

# Linux
RUN apt-get update && \
  apt-get install -y cron gnupg nginx && \
  apt-get install -y --fix-missing openssh-server

# Install Cloud66 Toolbelt
RUN curl -sSL https://s3.amazonaws.com/downloads.cloud66.com/cx_installation/cx_install.sh | bash

# Install kubectl
RUN apt-get update && apt-get install -y apt-transport-https && \
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list && \
  apt-get update && apt-get install -y kubectl

# Switch back to notebook user
USER $NB_UID

# Install Python Dependencies
RUN pip install jupyter_contrib_nbextensions
USER root
RUN jupyter contrib nbextension install
USER $NB_UID
RUN pip install recordlinkage pyjarowinkler
RUN conda install -y gspread oauth2client python-dotenv papermill nb_conda_kernels jupytext pandas=0.24.2

# Install Docker & ZSH
USER root
RUN sudo apt-get update && sudo apt-get install -y lsb-release software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable" && \
    apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

RUN sudo apt-get update && sudo apt-get -y install zsh vim
USER $NB_UID

# Copy hooks
COPY start_notebook.sh /usr/local/bin/start-notebook.d/start_notebook.sh
COPY before_notebook.sh /usr/local/bin/before-notebook.d/before_notebook.sh

EXPOSE 8888