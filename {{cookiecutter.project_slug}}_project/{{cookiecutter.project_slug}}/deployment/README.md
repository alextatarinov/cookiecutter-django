# Packages
sudo apt-get update && sudo apt-get install nginx python3-pip postgresql postgresql-client libpq-dev supervisor nano git redis-server

# DB
sudo -su postgres psql
CREATE DATABASE {{ cookiecutter.project_slug }};
# Set password here
CREATE USER {{ cookiecutter.project_slug }} WITH PASSWORD ;
GRANT ALL PRIVILEGES ON DATABASE {{ cookiecutter.project_slug }} TO {{ cookiecutter.project_slug }};

# Folders
mkdir {{ cookiecutter.project_slug }}_project
cd {{ cookiecutter.project_slug }}_project
# Git url here
git clone
mkdir nginx gunicorn
# Folders for local files storage
mkdir static media

# Virtualenv
pip3.6 install virtualenv
virtualenv --no-site-packages --python=python3.6 venv
source venv/bin/activate
cd {{ cookiecutter.project_slug }}
pip install --upgrade pip
pip install -r req*

# Configs - move to folders
gunicorn.conf.py - /home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn
nginx.conf - /etc/nginx
default - /etc/nginx/sites-available/
{{ cookiecutter.project_slug}}.conf, celery.conf - /etc/supervisor/conf.d/
ffdhe2048.dh - /etc/nginx/

# Generate self-signed SSL certificate with common name * for default_server
sudo openssl req -x509 -nodes -days 9999 -newkey rsa:2048 -keyout /etc/nginx/nginx.key -out /etc/nginx/nginx.crt

# Set permissions for read-write folders
cd ..
sudo chown www-data static media logs nginx
sudo chmod 755 static media logs nginx

# Create SSL certificates
sudo add-apt-repository ppa:certbot/certbot && sudo apt-get update && sudo apt-get install certbot 
sudo certbot certonly --standalone --pre-hook "service nginx stop" --post-hook "service nginx start" --rsa-key-size=4096 --must-staple
# Add renew script to crontab 
crontab -e
certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start" --rsa-key-size=4096 --must-staple

# Enable nginx config
sudo service nginx restart

# Enable supervisor config
sudo supervisorctl update
