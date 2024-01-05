# https://docs.gunicorn.org/en/stable/settings.html#settings
import multiprocessing

max_requests = 0
max_requests_jitter = 0

log_file = "-"

workers = multiprocessing.cpu_count() * 2 + 1
# workers = 3
