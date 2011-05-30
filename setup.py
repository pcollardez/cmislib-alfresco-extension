import os
from setuptools import setup, find_packages

version = '0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cmislib-alfresco-extension",
    description = 'Apache Chemistry CMIS client library Alfresco extension for Python',
    version = version,
    author = 'Patrice Collardez',
    author_email = 'pcollardez@acxio.fr',
    license = 'Apache License (2.0)',
    url = 'http://www.acxio.fr/',
    package_dir = {'':'src'},
    packages = find_packages('src', exclude=['tests']),
    #include_package_data = True,
    exclude_package_data = {'':['tests']},
    zip_safe = False,
    install_requires = ('cmislib'),
    long_description = read('README.txt'),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        ],
)
