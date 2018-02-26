import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/gunicorn.pid'
accesslog = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/access.log'
errorlog = '/home/ubuntu/{{ cookiecutter.project_slug }}_project/gunicorn/access.log'
capture_output = True
user = 'www-data'
