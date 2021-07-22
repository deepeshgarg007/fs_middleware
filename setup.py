from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in fs_middleware/__init__.py
from fs_middleware import __version__ as version

setup(
	name='fs_middleware',
	version=version,
	description='Test',
	author='deepesh@erpnext.com',
	author_email='hello@erpnext.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
