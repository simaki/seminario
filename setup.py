# coding: utf-8

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='seminario',
    version='0.2.0',
    description='Python package for seminar organization.',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    author='Shota Imaki',
    author_email='shota.imaki@icloud.com',
    maintainer='Shota Imaki',
    maintainer_email='shota.imaki@icloud.com',
    url='https://github.com/simaki/seminario',
    packages=['seminario'],
    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
