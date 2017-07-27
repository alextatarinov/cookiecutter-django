from fabric.api import *
import os

env.key_filename = None
env.user = 'ubuntu'
env.hosts = []

project_dir = '/home/{{project_name}}/{{project_name}}_project/'
app_dir = os.path.join(project_dir, {{project_name}})
env_dir = os.path.join(project_dir, 'venv')


def deploy():
    with prefix('source ' + os.path.join(env_dir, 'bin', 'activate')):
        with cd(project_dir):
            run('git pull')
            run('pip install -r requirements.txt')
        with cd(app_dir):
            run('python manage.py migrate')
            run('python manage.py collectstatic --no-input')
    sudo('supervisorctl reload ' + {{project_name}})
