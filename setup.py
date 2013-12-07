from setuptools import setup, find_packages

setup(
    name         = 'scrapy_weibo_v1',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = scrapy_weibo.settings']},
)