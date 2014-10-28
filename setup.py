from distutils.core import setup
setup(
name = 'minickt',
packages = ['minickt', 'cktParser', 'cktWriter'],
scripts = ['minic'],
install_requires=['matplotlib','networkx'],
version = '0.8.5',
description = 'Analyzer and simulator of logic circuit',
author = 'dokelung',
author_email = 'dokelung@gmail.com',
url = 'https://github.com/dokelung/minickt',
download_url = 'https://github.com/dokelung/minickt/tarball/v0.8.5',
keywords = ['circuit','eda','verification','logic','gate'],
classifiers = [],
)
