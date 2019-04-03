# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup

here = Path(__file__).parent

about = {}
with Path(here, 'diff_1c', '__about__.py').open() as f:
    exec(f.read(), about)

setup(
    name='diff-1c',
    version=about['__version__'],
    description='Diff utility for 1C:Enterprise',
    author='Cujoko',
    author_email='cujoko@gmail.com',
    url='https://github.com/Cujoko/diff-1c',
    packages=['diff_1c'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords='1c diff v8reader v8unpack gcomp',
    entry_points={
        'console_scripts': [
            'diff1c=diff_1c.__main__:run'
        ]
    },
    license='MIT',
    install_requires=[
        'cjk-commons>=3.3.0',
        'parse-1c-build>=5.5.0'
    ]
)
