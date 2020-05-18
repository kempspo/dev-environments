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
    location ~* (/user/[^/]*)/api/kernels/ {
        proxy_pass            https://jupyter;
        proxy_set_header      Host $http_host;
        # websocket support
        proxy_http_version    1.1;
        proxy_set_header      Upgrade "websocket";
        proxy_set_header      Connection "Upgrade";
        proxy_read_timeout    86400;
    }
    location ~* (/user/[^/]*)/terminals/ {
        proxy_pass            http://jupyter;
        proxy_set_header      Host $http_host;
        # websocket support
        proxy_http_version    1.1;
        proxy_set_header      Upgrade "websocket";
        proxy_set_header      Connection "Upgrade";
        proxy_read_timeout    86400;
    }    
}
" | sudo tee /etc/nginx/sites-enabled/default
sudo service nginx start