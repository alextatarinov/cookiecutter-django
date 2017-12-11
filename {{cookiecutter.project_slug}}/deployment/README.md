sudo apt-get install nginx python3-pip postgresql postgresql-client libpq-dev supervisor nano git

sudo adduser {{ cookiecutter.project_slug }}
# disable login
passwd -l {{ cookiecutter.project_slug }}

sudo -su postgres psql 
CREATE DATABASE {{ cookiecutter.project_slug }};
CREATE USER {{ cookiecutter.project_slug }} WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE {{ cookiecutter.project_slug }} TO {{ cookiecutter.project_slug }};

cd /home/{{ cookiecutter.project_slug }}

git clone https://bitbucket.org/tatarinov97/{{ cookiecutter.project_slug }}/
cd {{ cookiecutter.project_slug }}

mkdir nginx
mkdir gunicorn

pip3 install virtualenv

virtualenv --no-site-packages --python=python3 venv
pip install -r req*
pip install gunicorn

# if local storage is used
mkdir static
mkdir media

# Copy
gunicorn.conf.py - {{ cookiecutter.project_slug }}/gunicorn
nginx.conf - etc/nginx
default - /etc/nginx/sites-available/
project.conf - /etc/supervisor/conf.d/
ffdhe2048.dh - /etc/nginx/

# For permissions
# static, media folder - 755, owned by project user
# inside static and media folders run:
sudo find . -type d -exec sudo chmod 755 {} \;
sudo find . -type f -exec sudo chmod 644 {} \;
