from distutils.core import setup

setup(
	name = 'minickt',
	packages = ['minickt', 'cktParser', 'cktWriter'],
	scripts = ['minickt.py'],
	version = '0.6.8',
	description = 'Analyzer and simulator of logic circuit',
	author = 'dokelung',
	author_email = 'dokelung@gmail.com',
	url = 'https://github.com/dokelung/minickt',
	download_url = 'https://github.com/dokelung/minickt/tarball/v0.6.8',
	keywords = ['circuit','eda','verification','logic','gate'],
	classifiers = [],
)