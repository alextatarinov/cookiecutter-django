sudo apt-get install nginx python3-pip postgresql postgresql-client libpq-dev supervisor nano git

sudo adduser {{project_name}}
# disable login
passwd -l {{project_name}}

sudo -su postgres psql 
CREATE DATABASE {{project_name}};
CREATE USER {{project_name}} WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE {{project_name}} TO {{project_name}};

cd /home/{{project_name}}

git clone https://bitbucket.org/tatarinov97/{{project_name}}_project/
cd {{project_name}}_project

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
gunicorn.conf.py - {{project_name}}_project/gunicorn
nginx.conf - etc/nginx
default - /etc/nginx/sites-available/
project.conf - /etc/supervisor/conf.d/

# For permissions (use wisely)
# Is this really meaningfull???
#
# addgroup {{project_name}}-group
# usermod -a -G {{project_name}}-group {{project_name}}
# static, media folder - 755, owned by project user
# source folders - 750, source files 640, owned by root:{{project_name}}-group
# gunicorn folder - project user, 700 or 755
# nginx folder - www-data, 700 or 755

sudo find . -type d -exec sudo chmod 750 {} \;
sudo find . -type f -exec sudo chmod 640 {} \;
