# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='easygraph',
    version='0.1.1',
    url='https://github.com/naruminho/easyGraph',
    license='MIT License',
    author='Narumi Abe and Melissa Forti',
    author_email='mail.narumi@gmail.com',
    keywords='graph networks, plotly, networkx',
    description='A tool for plotting graph networks',
    packages=['easygraph'],
    install_requires=['pandas', 'plotly', 'networkx','matplotlib'],
)
