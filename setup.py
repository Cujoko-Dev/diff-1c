#! python3
# -*- coding: utf-8 -*-
import diff_1c
from setuptools import setup


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

        'Topic :: Software Development',
        'Topic :: Utilities'
    ],

    keywords='1c diff v8reader v8unpack gcomp',

    install_requires=[
        'appdirs>=1.4.3',
        'parse-1c-build>=2.0.0'
    ],

    py_modules=['diff-1c'],

    entry_points={
        'console_scripts': [
            'diff-1c=diff_1c:main'
        ]
    }
)

