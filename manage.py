import os
import sys

from django.core.exceptions import ImproperlyConfigured


def check_remote_db():
    # Check for remote database usage to prevent accidents with migrating production database
    settings_module = os.environ['DJANGO_SETTINGS_MODULE']
    is_local_run = 'prod' not in settings_module
    is_test_run = 'test' in sys.argv
    is_server_run = 'runserver' in sys.argv
    if is_local_run and not (is_test_run or is_server_run):
        local_db_used = settings.DATABASES['default']['HOST'] == '127.0.0.1'

        if not local_db_used:
            raise ImproperlyConfigured('Cannot run command on remote DATABASE')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.server')
    try:
        from django.core.management import execute_from_command_line  # noqa: WPS433
        from django.conf import settings  # noqa: WPS433
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:  # noqa: WPS505
            import django  # noqa: F401 WPS433
        except ImportError:
            raise ImportError(
                ''.join((
                    "Couldn't import Django. Are you sure it's installed and ",
                    'available on your PYTHONPATH environment variable? Did you ',
                    'forget to activate a virtual environment?'
                ))
            )
        raise

    check_remote_db()

    execute_from_command_line(sys.argv)
