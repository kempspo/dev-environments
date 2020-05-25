#! /bin/bash

# Turn JUPYTERHUB_USER into USER variable
export USER=$(echo ${JUPYTERHUB_USER})

# Add nginx config and start nginx
sudo rm -f /etc/nginx/sites-enabled/default
echo "
map \$http_upgrade \$connection_upgrade {
        default upgrade;
        '' close;
    }
server {
        listen 8888;
        listen [::]:8888;
        rewrite ^${JUPYTERHUB_SERVICE_PREFIX:0:(-1)}$ $HUB_HOST$JUPYTERHUB_SERVICE_PREFIX permanent;
        location $JUPYTERHUB_SERVICE_PREFIX {
             proxy_pass http://127.0.0.1:8080/;
             proxy_redirect http://127.0.0.1:8080/ $HUB_HOST$JUPYTERHUB_SERVICE_PREFIX;
             proxy_http_version 1.1;
             proxy_set_header Upgrade \$http_upgrade;
             proxy_set_header Connection \$connection_upgrade;
             proxy_read_timeout 20d;
             proxy_set_header Host \$host;
             proxy_set_header Accept-Encoding gzip;
        }
}
" > /etc/nginx/sites-enabled/default
sudo service nginx start

# Allow non root user to use docker
sudo usermod -aG docker coder
sudo mkdir -p /home/$USER
sudo chown -R 1000:1000 /home/$USER

# Run VS Code Server
sudo runuser -l  coder -c "\
    HOME=/home/$USER \
    /usr/bin/dumb-init \
    code-server \
    --auth none --disable-telemetry \
    "