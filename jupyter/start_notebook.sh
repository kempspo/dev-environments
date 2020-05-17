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
server {
    location ~ /api/kernels/ {
            proxy_pass            http://notebook;
            proxy_set_header      Host \$host;
            # websocket support
            proxy_http_version    1.1;
            # proxy_set_header      Upgrade "websocket";
            # proxy_set_header      Connection "Upgrade";
            proxy_set_header      Upgrade \$http_upgrade;
            proxy_set_header      Connection \$connection_upgrade;
            proxy_read_timeout    86400;
        }
    location ~ /terminals/ {
            proxy_pass            http://notebook;
            proxy_set_header      Host \$host;
            # websocket support
            proxy_http_version    1.1;
            # proxy_set_header      Upgrade "websocket";
            # proxy_set_header      Connection "Upgrade";
            proxy_set_header      Upgrade \$http_upgrade;
            proxy_set_header      Connection \$connection_upgrade;
            proxy_read_timeout    86400;
    }    
}
" | sudo tee /etc/nginx/sites-enabled/default
sudo service nginx start