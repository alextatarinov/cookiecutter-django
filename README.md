## Setup linter
    flake8 --install-hook git
    git config --bool flake8.strict true

## Checklist
### Local only
- setup pycharm to use settings.local
- update all project paths and names
- configure Jenkins (add bitbucket webhook)
- setup dns

### Both local and server
- create venv
- install dependencies
- create .env from deploy/.env.example
- create database and update .env DATABASE_URL
- generate SECRET_KEY for .env
- install rabbitmq and redis

### Server only
- setup or remove email config for .env and settings.server
- setup Sentry and .env SENTRY_DNS
- generate ssl certificates
- remove default nginx config
