#! /bin/bash

# Turn JUPYTERHUB_USER into USER variable
export USER=$(echo ${NB_USER})

# Add nginx config and start nginx
echo "
map \$http_upgrade \$connection_upgrade {
        default upgrade;
        '' close;
    }
server {
        listen 8888;
        listen [::]:8888;
        # Allow to upload files up to 2GB
        client_max_body_size 2G;
        rewrite ^${JUPYTERHUB_SERVICE_PREFIX:0:(-1)}$ $HUB_HOST$JUPYTERHUB_SERVICE_PREFIX permanent;
        location $JUPYTERHUB_SERVICE_PREFIX {
             proxy_pass http://127.0.0.1:8787/;
             proxy_redirect http://127.0.0.1:8787/ $HUB_HOST$JUPYTERHUB_SERVICE_PREFIX;
             proxy_http_version 1.1;
             proxy_set_header Upgrade \$http_upgrade;
             proxy_set_header Connection \$connection_upgrade;
             proxy_read_timeout 20d;
        }
}
" > /etc/nginx/sites-enabled/default
service nginx start

# Allow non root user to use docker
usermod -aG docker $USER

# Get root environment and place in system-wide Renviron file
R_ENVIRON=$(Rscript -e "cat(R.home())")/etc/Renviron.site
env > $R_ENVIRON

# Remove sensitive enrivonment variables
sed -i '/^HOME=/d' $R_ENVIRON
sed -i '/^PWD=/d' $R_ENVIRON
sed -i '/^PATH=/d' $R_ENVIRON
sed -i '/^USER=/d' $R_ENVIRON
sed -i '/^PASSWORD=/d' $R_ENVIRON

# Run original script
/init