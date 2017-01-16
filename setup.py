from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

setup(
    name='rstwriter',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'dist']),
    install_requires=['docutils'],
    version='0.8.3',
    description='A report writer powered with reStructuredText for Pandas library.',
    author='Rafael Alves Ribeiro',
    author_email='rafael.alves.ribeiro@gmail.com',
    license='MIT',
    url='https://github.com/rafpyprog/rstwriter',
    download_url='https://github.com/rafpyprog/rstwriter/tarball/0.8.3',
    keywords=['reStructuredText', 'rst', 'pandas', 'reporting'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5'.
    ),
)
