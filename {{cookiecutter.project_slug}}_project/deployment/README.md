# Packages
sudo apt-get install nginx python3-pip postgresql postgresql-client libpq-dev supervisor nano git redis-server

# DB
sudo -su postgres psql
CREATE DATABASE {{ cookiecutter.project_slug }};
# Set password here
CREATE USER {{ cookiecutter.project_slug }} WITH PASSWORD ;
GRANT ALL PRIVILEGES ON DATABASE {{ cookiecutter.project_slug }} TO {{ cookiecutter.project_slug }};

# Folders
mkdir {{ cookiecutter.project_slug }}_project
# Git url here
git clone
cd {{ cookiecutter.project_slug }}
mkdir nginx gunicorn
# Folders for local files storage
mkdir static media

# Virtualenv
pip3.6 install virtualenv
virtualenv --no-site-packages --python=python3.6 venv
pip install -r req*
source venv/bin/activete

# Configs - move to folders
gunicorn.conf.py - /home/ubuntu/{{ cookiecutter.project_slug }}/gunicorn
nginx.conf - /etc/nginx
default - /etc/nginx/sites-available/
project.conf - /etc/supervisor/conf.d/
ffdhe2048.dh - /etc/nginx/

# Generate self-signed SSL certificate with common name * for default_server
sudo openssl req -x509 -nodes -days 9999 -newkey rsa:2048 -keyout /etc/nginx/nginx.key -out /etc/nginx/nginx.crt

# Set permissions for static and media
sudo chown www-data static media
sudo chmod 755 static media

# Enable nginx config
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
sudo service nginx restart

# Enable supervisor config
sudo supervisorctl update
