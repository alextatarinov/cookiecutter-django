from fabric.api import *
import os


env.key_filename = '~/.ssh/aws-{{ cookiecutter.project_slug }}.pem'
env.user = 'ubuntu'
env.hosts = ['{{ cookiecutter.domain_name }}']

project_dir = '/home/ubuntu/{{ cookiecutter.project_slug }}_project'
app_dir = os.path.join(project_dir, '{{ cookiecutter.project_slug }}')
env_dir = os.path.join(project_dir, '.venv')


def deploy():
    with prefix('source ' + os.path.join(env_dir, 'bin', 'activate')):
        with cd(project_dir):
            run('git pull')
            run('pip install -r requirements.txt')
        with cd(app_dir):
            run('python manage.py migrate')
            run('python manage.py collectstatic --no-input')

    sudo('supervisorctl reload {}'.format('{{ cookiecutter.project_slug }}'))
