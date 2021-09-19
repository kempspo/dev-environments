# Configuration file for jupyterhub.

# Package Imports
from os import environ
from json import loads
from ast import literal_eval
from oauthenticator.google import LocalGoogleOAuthenticator
from kubespawner.spawner import KubeSpawner

## Grant admin users permission to access single-user servers.
#  
#  Users should be properly informed if this is enabled.
c.JupyterHub.admin_access = True

## The URL on which the Hub will listen. This is a private URL for internal
#  communication. Typically set in combination with hub_connect_url. If a unix
#  socket, hub_connect_url **must** also be set.
#  
#  For example:
#  
#      "http://127.0.0.1:8081"
#      "unix+http://%2Fsrv%2Fjupyterhub%2Fjupyterhub.sock"
#  
#  .. versionadded:: 0.9
c.JupyterHub.hub_bind_url = 'http://0.0.0.0:8081'

## The URL for connecting to the Hub. Spawners, services, and the proxy will
#  use this URL to talk to the Hub.
#  
#  Only needs to be specified if the default hub URL is not connectable (e.g.
#  using a unix+http:// bind url).
#  
#  .. seealso::
#      JupyterHub.hub_connect_ip
#      JupyterHub.hub_bind_url
#  
#  .. versionadded:: 0.9
c.JupyterHub.hub_connect_url = environ['HUB_CONNECT_URL']

## The public facing port of the proxy.
#  
#  This is the port on which the proxy will listen. This is the only port
#  through which JupyterHub should be accessed by users.
#  
#  .. deprecated: 0.9
#      Use JupyterHub.bind_url
c.JupyterHub.port = 8000

## The class to use for spawning single-user servers. 
#  
#  Should be a subclass of Spawner.
c.JupyterHub.spawner_class = KubeSpawner

# This allows people to name the servers and thus spin up multiple servers.
c.JupyterHub.allow_named_servers = True

# KuberSpawner config statements
c.KubeSpawner.image = 'jupyter/all-spark-notebook:bfb2be718a58'
c.KubeSpawner.namespace = environ['CLOUD66_STACK_NAMESPACE']

# This is the docker image pull secrets to pull from private repos.
c.KubeSpawner.image_pull_secrets = 'regcred'

# Add extra RStudio environment options for KubeSpawner to ingest.
rstudio_environ = {
    'PASSWORD': 'test',
    'DISABLE_AUTH': 'true',
    'ROOT': 'true'
}

# Merge current environ list with the additional RStudio environs.
environ_list = {**rstudio_environ, **environ}

# Blacklist of environment variables that should not be passed down to the 
# individual single servers.
environ_blacklist = [
    'CLOUD66_SERVER_NAME',
    'LS_COLORS',
    'JUPYTERHUB_EXTERNAL_PORT_8000_TCP_ADDR',
    'CLOUD66_SERVICE_GIT_BRANCH',
    'LESSCLOSE',
    'JUPYTERHUB_PORT_8081_UDP',
    'JUPYTERHUB_SERVICE_PORT',
    'CLOUD66_STACK_NAMESPACE',
    'LANG',
    'OAUTH_CLIENT_ID',
    'HOSTNAME',
    'CLOUD66_ACCOUNT_KEY',
    'WEB_ADDRESS',
    'CLOUD66_STACK_EXTERNAL_IPS',
    'JUPYTERHUB_PORT_8081_TCP_ADDR',
    'OAUTH_CLIENT_SECRET',
    'WEB_ADDRESSES_INT',
    'KUBERNETES_PORT_443_TCP_PROTO',
    'KUBERNETES_PORT_443_TCP_ADDR',
    'DOCKER_HOST_IP_MASTER',
    'KUBERNETES_PORT',
    'WEB_ADDRESS_EXT',
    'PWD',
    'HOME',
    'JUPYTERHUB_PORT_8081_UDP_PROTO',
    'JUPYTERHUB_EXTERNAL_PORT_8000_TCP',
    'WEB_ADDRESSES_EXT',
    'KUBERNETES_SERVICE_PORT_HTTPS',
    'DEBIAN_FRONTEND',
    'CLOUD66_SECRET_KEY',
    'KUBERNETES_PORT_443_TCP_PORT',
    'JUPYTERHUB_EXTERNAL_PORT_8000_TCP_PROTO',
    'OAUTH_CALLBACK_URL',
    'JUPYTERHUB_PORT_8081_TCP_PROTO',
    'FAILOVER_STATUS',
    'JUPYTERHUB_SERVICE_HOST',
    'JUPYTERHUB_EXTERNAL_PORT',
    'JUPYTERHUB_PORT_8081_TCP_PORT',
    'WEB_ADDRESS_INT',
    'KUBERNETES_PORT_443_TCP',
    'CLOUD66_SERVER_EXTERNAL_IP_MASTER',
    'CLOUD66_STACK_NAME',
    'TERM',
    'CLOUD66_SERVICE_NAME',
    'JUPYTERHUB_EXTERNAL_SERVICE_PORT',
    'JUPYTERHUB_PORT_8081_UDP_ADDR',
    'JUPYTERHUB_PORT_8081_TCP',
    'SHLVL',
    'CLOUD66_SERVICE_DOCKERFILE',
    'JUPYTERHUB_EXTERNAL_SERVICE_HOST',
    'WEB_ADDRESSES',
    'KUBERNETES_SERVICE_PORT',
    'JUPYTERHUB_EXTERNAL_PORT_8000_TCP_PORT',
    'JUPYTERHUB_PORT',
    'JUPYTERHUB_PORT_8081_UDP_PORT',
    'JUPYTERHUB_EXTERNAL_SERVICE_PORT_JUPYTERHUB_8000',
    'JUPYTERHUB_SERVICE_PORT_JUPYTERHUB_8081',
    'PATH',
    'KUBERNETES_SERVICE_HOST',
    'SECRET_KEY_BASE',
    'CLOUD66_SERVICE_GIT_REPO',
    'JUPYTERHUB_SERVICE_PORT_JUPYTERHUB_8081_UDP',
    'LESSOPEN',
    'CLOUD66_SERVICE_GIT_REF',
    'ADMIN_LIST',
    'SPAWN_LIST'
]

# Loop through the blacklist to filter out environment variables.
for i in environ_blacklist:
    if i in environ_list.keys():
        del environ_list[i]

# KubeSpawner config settings (volume mounts and passing env variables)
c.KubeSpawner.environment = environ_list
c.KubeSpawner.volume_mounts = [
    {"mountPath": "/home/{username}", "name": "home"},
    {"mountPath": "/var/run/docker.sock", "name": "docker"},
    {"mountPath": "/mnt/envs", "name": "envs"},
    {"mountPath": "/home/envs/{username}", "name": "airflow-envs"}
]
c.KubeSpawner.volumes = [
    {
        "name": "home",
        "hostPath": {
            "path": "/mnt/data-store/home/{username}",
            "type": "DirectoryOrCreate"
        }
    },
    {
        "name": "docker",
        "hostPath": {
            "path": "/var/run/docker.sock",
            "type": "Socket"
        }
    },
    {
        "name": "envs",
        "hostPath": {
            "path": "/mnt/data-store/envs",
            "type": "DirectoryOrCreate"
        }
    },
    {
        "name": "airflow-envs",
        "hostPath": {
            "path": "/mnt/data-store/envs/{username}",
            "type": "DirectoryOrCreate"
        }
    }
]

c.KubeSpawner.profile_list = loads(environ['SPAWN_LIST'])

## Timeout (in seconds) before giving up on starting of single-user server.
#  
#  This is the timeout for start to return, not the timeout for the server to
#  respond. Callers of spawner.start will assume that startup has failed if it
#  takes longer than this. start should return when the server process is
#  started and its location is known.
c.KubeSpawner.start_timeout = 60 * 10
c.KubeSpawner.http_timeout = 60 * 10

## Set of users that will have admin rights on this JupyterHub.
#  
#  Admin users have extra privileges:
#   - Use the admin panel to see list of users logged in
#   - Add / remove users in some authenticators
#   - Restart / halt the hub
#   - Start / stop users' single-user servers
#   - Can access each individual users' single-user server (if configured)
#  
#  Admin access should be treated the same way root access is.
#  
#  Defaults to an empty set, in which case no user has admin access.
c.Authenticator.admin_users = set(literal_eval(environ['ADMIN_LIST']))
c.Authenticator.whitelist = set(literal_eval(environ['WHITELIST']))

# Google OAuth Implementation
c.JupyterHub.authenticator_class = LocalGoogleOAuthenticator
c.LocalGoogleOAuthenticator.oauth_callback_url = environ['OAUTH_CALLBACK_URL']
c.LocalGoogleOAuthenticator.client_id = environ['OAUTH_CLIENT_ID']
c.LocalGoogleOAuthenticator.client_secret = environ['OAUTH_CLIENT_SECRET']
c.GoogleOAuthenticator.hosted_domain = ['gmail.com']

## Automatically begin the login process
#  
#  rather than starting with a "Login with..." link at `/hub/login`
#  
#  To work, `.login_url()` must give a URL other than the default `/hub/login`,
#  such as an oauth handler or another automatic login handler, registered with
#  `.get_handlers()`.
#  
#  .. versionadded:: 0.8
c.Authenticator.auto_login = True

## The command to use for creating users as a list of string
#  
#  For each element in the list, the string USERNAME will be replaced with the
#  user's username. The username will also be appended as the final argument.
#  
#  For Linux, the default value is:
#  
#      ['adduser', '-q', '--gecos', '""', '--disabled-password']
#  
#  To specify a custom home directory, set this to:
#  
#      ['adduser', '-q', '--gecos', '""', '--home', '/customhome/USERNAME', '--
#  disabled-password']
#  
#  This will run the command:
#  
#      adduser -q --gecos "" --home /customhome/river --disabled-password river
#  
#  when the user 'river' is created.
c.LocalAuthenticator.add_user_cmd = ['adduser', '--force-badname']

## If set to True, will attempt to create local system users if they do not
#  exist already.
#  
#  Supports Linux and BSD variants only.
c.LocalAuthenticator.create_system_users = True

# Use same default service account as the spawner
c.KubeSpawner.service_account = 'default'

# Add extra labels so that pod expose exposes a unique pod
c.KubeSpawner.extra_labels = {
    'username': '{username}'
}