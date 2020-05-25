#! /bin/bash

# Export NB_USER
export NB_USER=$(echo $NB_USER)

# replace conda envs folder with persistent envs folder
rm -rf /opt/conda/envs
mkdir -p /mnt/envs
ln -s /mnt/envs /opt/conda/envs
sudo chown -R 1000:100 /opt/conda/envs

jupyter notebook --generate-config -y
echo 'c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"' >> ~/.jupyter/jupyter_notebook_config.py

# Give nb user docker permissions
sudo usermod -aG docker $NB_USER

cd /home