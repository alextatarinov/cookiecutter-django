import os


# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def remove_celery():
    """Removes the celery.py if celery isn't going to be used"""
    celery_location = os.path.join(
        PROJECT_DIRECTORY,
        '{{ cookiecutter.project_slug }}/celery.py'
    )
    remove_file(celery_location)


# Removes the celery.py if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_celery()
