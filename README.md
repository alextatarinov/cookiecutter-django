## Setup
#### Create virtualenv and install packages  
    source venv/bin/activate  
    poetry install  
    
    flake8 --install-hook git
    git config --bool flake8.strict true

Use config.settings.local for local development. Note that this file is included to Git

#### DB (set good password for production)
    sudo -su postgres psql  
    CREATE DATABASE clevergames;  
    CREATE USER clevergames WITH PASSWORD 'clevergames';  
    GRANT ALL PRIVILEGES ON DATABASE clevergames TO clevergames;  
    ALTER USER clevergames createdb;


#### After server clone
- setup dns
- add Jenkinsfile configs
- obtain new certificate  
- edit .env file 
- restart build
