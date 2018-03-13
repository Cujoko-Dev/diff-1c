# -*- coding: utf-8 -*-
from setuptools import setup

import diff_1c

setup(
    name='diff_1c',

    version=diff_1c.__version__,

    description='Diff utility for 1C:Enterprise',

    url='https://github.com/Cujoko/diff-1c',

    author='Cujoko',
    author_email='cujoko@gmail.com',

    license='MIT',

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

    install_requires=[
        'commons',
        'parse-1c-build'
    ],

    dependency_links=[
        'http://github.com/Cujoko/commons/tarball/master',
        'http://github.com/Cujoko/parse-1c-build/tarball/master'
    ],

    py_modules=['diff-1c'],

    entry_points={
        'console_scripts': [
            'diff1c=diff_1c.__main__:run'
        ]
    }
)
