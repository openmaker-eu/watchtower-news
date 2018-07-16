"""
This is the settings file for Watchtower.
"""
__author__ = ['Enis Simsar', 'Kemal Berk Kocabagli']

# import random
# import string
from tornado.options import define
from decouple import config

define("port", default=config("HOST_PORT"), help="run on the given port", type=int)

# chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace(
#     '\\', '')
# secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(100)])
secret_key = 'PEO+{+RlTK[3~}TS-F%[9J/sIp>W7!r*]YV75GZV)e;Q8lAdNE{m@oWK.+u-&z*-p>~Xa!Z8j~{z,BVv.e0GChY{(1.KVForO#rQ'

settings = dict(
    xsrf_cookies=False,
    cookie_secret=secret_key,
)