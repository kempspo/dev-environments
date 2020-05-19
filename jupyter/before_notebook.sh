#! /bin/bash

# Export NB_USER
export NB_USER=$(echo $NB_USER)

jupyter notebook --generate-config -y
echo 'c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"' >> ~/.jupyter/jupyter_notebook_config.py

# Give nb user docker permissions
sudo usermod -aG docker $NB_USER

cd /home