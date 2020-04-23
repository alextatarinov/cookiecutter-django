import multiprocessing


bind = 'unix:/tmp/gunicorn.sock'
accesslog = '-'
workers = multiprocessing.cpu_count() * 2 + 1
user = 'ubuntu'
timeout = 600
