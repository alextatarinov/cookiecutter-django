from fabric.api import *
import os


env.key_filename = None
env.user = 'ubuntu'
env.hosts = []

project_dir = '/home/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}'
app_dir = os.path.join(project_dir, {{ cookiecutter.project_slug }})
env_dir = os.path.join(project_dir, '.venv')


def deploy():
    with prefix('source ' + os.path.join(env_dir, 'bin', 'activate')):
        with cd(project_dir):
            run('git pull')
            run('pip install -r requirements.txt')
        with cd(app_dir):
            run('python manage.py migrate')
            {% if cookiecutter.use_s3 == 'y' %}
            run('python manage.py fasts3collectstatic --no-input')
            {% else %}
            run('python manage.py collectstatic --no-input')
            {% endif %}

    sudo('supervisorctl reload {}'.format({{ cookiecutter.project_slug }}))
