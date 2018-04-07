# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import diff_1c

setup(
    name='diff_1c',
    version=diff_1c.__version__,
    description='Diff utility for 1C:Enterprise',
    author='Cujoko',
    author_email='cujoko@gmail.com',
    url='https://github.com/Cujoko/diff-1c',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords='1c diff v8reader v8unpack gcomp',
    entry_points={
        'console_scripts': [
            'diff1c=diff_1c.__main__:run'
        ]
    },
    license='MIT'
)
