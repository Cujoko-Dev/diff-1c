#! python3
# -*- coding: utf-8 -*-
import diff1c
from setuptools import setup


setup(
    name='diff1c',

    version=diff1c.__version__,

    description='Diff utility for 1C:Enterprise',

    url='https://github.com/Cujoko/diff1c',

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

    py_modules=['diff1c'],

    entry_points={
        'console_scripts': [
            'diff1c=diff1c:main'
        ]
    }
)

