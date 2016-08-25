# python setup.py --dry-run --verbose install

from distutils.core import setup


setup(
    name='pywirelesstags',
    version='0.5.1', # Should be updated with new versions
    author='Wojtek Widurek',
    author_email='wwidurek@gmail.com',
    py_modules=['wirelesstag'],
    scripts=[],
    data_files=[],
    url='https://github.com/wwidurek/wirelesstag',
    license='Open Source',
    description='Simple API to access WirelessTag data from any python script.',
    long_description=open('README.md').read()
)
