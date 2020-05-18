#! /bin/bash

# Export NB_USER
export NB_USER=$(echo $NB_USER)

# change default shell
export SHELL=`which zsh`

# Add nginx config and start nginx
sudo rm -f /etc/nginx/sites-enabled/default
echo "
map \$http_upgrade \$connection_upgrade {
        default upgrade;
        '' close;
    }
upstream notebook {
    server http://127.0.0.1:8888;
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
    location ~* (/user/[^/]*)/api/kernels/ {
        proxy_pass            http://127.0.0.1:8080/;
        proxy_set_header Host \$host;
        # websocket support
        proxy_http_version    1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \$connection_upgrade;
        proxy_read_timeout    86400;
    }
    location ~* (/user/[^/]*)/terminals/ {
        proxy_pass            http://127.0.0.1:8080/;
        proxy_set_header Host \$host;
        # websocket support
        proxy_http_version    1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \$connection_upgrade;
        proxy_read_timeout    86400;
    }    
}
" | sudo tee /etc/nginx/sites-enabled/default
sudo service nginx start