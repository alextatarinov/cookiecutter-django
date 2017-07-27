import os
import random
import shutil
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
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system."
        " Please change change your SECRET_KEY variables in conf/settings/dev.py and env.example"
        " manually."
    )
    return "CHANGEME!!"


def set_secret_key(setting_file_location):
    # Open locals.py
    with open(setting_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace('CHANGEME!!!', SECRET_KEY, 1)

    # Write the results to the locals.py module
    with open(setting_file_location, 'w') as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""
    # Determine the local_setting_file_location
    local_setting = os.path.join(
        project_directory,
        'config/settings/dev.py'
    )

    # dev.py settings file
    set_secret_key(local_setting)

    env_file = os.path.join(
        project_directory,
        'env.example'
    )

    # env.example file
    set_secret_key(env_file)


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


def remove_certbot_files():
    """
    Removes files needed for certbot if it isn't going to be used
    """
    nginx_dir_location = os.path.join(PROJECT_DIRECTORY, 'compose/nginx')
    for filename in ["nginx-secure.conf", "start.sh", "dhparams.example.pem"]:
        file_name = os.path.join(nginx_dir_location, filename)
        remove_file(file_name)


# Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# Removes the celery.py if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_celery()

# Removes all certbot/letsencrypt files if it isn't going to be used
if '{{ cookiecutter.use_lets_encrypt }}'.lower() != 'y':
    remove_certbot_files()
