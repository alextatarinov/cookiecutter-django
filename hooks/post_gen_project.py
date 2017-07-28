import os
import random
import string


# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        return ''.join(random.choice(
            string.digits + string.ascii_letters + punctuation
        ) for i in range(length))

    print(
        'Cookiecutter Django couldn\'t find a secure pseudo-random number generator on your system.'
        ' Please change change your SECRET_KEY variables in conf/settings/dev.py and env.example'
        ' manually.'
    )
    return 'CHANGEME!!'


def make_secret_key(project_directory):
    print(get_random_string())
    print(get_random_string())


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


# Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# Removes the celery.py if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_celery()
