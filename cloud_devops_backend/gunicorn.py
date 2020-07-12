# @Time    : 2020/7/12 14:26
# @Author  : ZhangEnmin
# @FileName: gunicorn.py
# @Software: PyCharm


from multiprocessing import cpu_count

bind="127.0.0.1:8000"
workers = cpu_count()
timeout = 60
graceful_timeout = 10
loglevel = "error"
errorlog = "/var/log/re_xops/xops.log"