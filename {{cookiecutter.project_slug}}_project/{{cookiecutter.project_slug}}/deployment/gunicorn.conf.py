import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/gunicorn.pid'
user = 'www-data'

accesslog = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/.fake_gunicorn_log'
access_log_format = '"%%(m)s %%(U)s %%(q)s %%(H)s" %%(s)s %%(b)s'
errorlog = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/.fake_gunicorn_log'
capture_output = True
