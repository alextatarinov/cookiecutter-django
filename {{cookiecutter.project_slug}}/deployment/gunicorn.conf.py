import multiprocessing

bind = "unix:/tmp/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = '/home/{{project_name}}/{{project_name}}_project/gunicorn/gunicorn.pid'
accesslog = '/home/{{project_name}}/{{project_name}}_project/gunicorn/access.log'
errorlog = '/home/{{project_name}}/{{project_name}}_project/gunicorn/access.log'
capture_output = True
user = '{{project_name}}'
