# python setup.py --dry-run --verbose install

from setuptools import setup


setup(
    name='wirelesstag',
    version='0.5.2', # Should be updated with new versions
    author='Wojtek Widurek',
    author_email='wwidurek@gmail.com',
    packages=['wirelesstag'],
    url='https://github.com/wwidurek/wirelesstag',
    license='Open Source',
    description='Simple API to access WirelessTag data from any python script.',
    zip_safe=False
)
