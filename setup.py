from distutils.core import setup

setup(
	name = 'minickt',
	packages = ['minickt', 'cktParser', 'cktWriter'],
	scripts = ['minic'],
	version = '0.7.0',
	description = 'Analyzer and simulator of logic circuit',
	author = 'dokelung',
	author_email = 'dokelung@gmail.com',
	url = 'https://github.com/dokelung/minickt',
	download_url = 'https://github.com/dokelung/minickt/tarball/v0.7.0',
	keywords = ['circuit','eda','verification','logic','gate'],
	classifiers = [],
)