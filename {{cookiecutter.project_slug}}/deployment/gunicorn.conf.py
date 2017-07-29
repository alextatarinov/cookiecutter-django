import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = '/home/{{ cookiecutter.project_slug }}/gunicorn/gunicorn.pid'
accesslog = '/home/{{ cookiecutter.project_slug }}/gunicorn/access.log'
errorlog = '/home/{{ cookiecutter.project_slug }}/gunicorn/access.log'
capture_output = True
user = '{{ cookiecutter.project_slug }}'
