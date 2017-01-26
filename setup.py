from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Nimble',

    version='0.1.0',

    description='Make getting data in batches easy.',
    long_description=long_description,

    url='https://github.com/risteon/nimble',

    author='Christoph Rist',
    author_email='c.rist@posteo.de',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha', 

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['imageio', 'scipy', 'pillow', 'six'],
    tests_require=['pytest'],
)
