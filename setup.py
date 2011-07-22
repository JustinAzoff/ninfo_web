from setuptools import setup, find_packages
import sys, os
from glob import glob


version = '0.1.0'

setup(name='ninfo_web',
    version=version,
    description="Simple web interface for ninfo",
    keywords='ninfo web',
    author='Justin Azoff',
    author_email='JAzoff@uamail.albany.edu',
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "bottle",
        "ninfo>=0.1.0",
        "repoze.who",
    ],
    entry_points = {
        'console_scripts': [
            'ninfo-web = ninfo_web:main',
        ]
    },
)
