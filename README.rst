===============================
pipit
===============================


.. image:: https://img.shields.io/pypi/v/pipit.svg
        :target: https://pypi.python.org/pypi/pipit

.. image:: https://img.shields.io/travis/youngking/pipit.svg
        :target: https://travis-ci.org/youngking/pipit

.. image:: https://readthedocs.org/projects/pipit/badge/?version=latest
        :target: https://pipit.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/youngking/pipit/shield.svg
     :target: https://pyup.io/repos/github/youngking/pipit/
     :alt: Updates


A package manager for python, based on pip


* Free software: Apache Software License 2.0
* Documentation: https://pipit.readthedocs.io.


Features
--------

* download, build and cache wheel packages
* generate console scripts like `zc.buildout`

Quick Start
------------

* install pipit from pypi

  `pip install pipit`


* To build, just run `pipit` in your project root, and pipit will fetch the new dependencies
  and all of their dependencies, according to the `setup.py` and `requirements.txt`

  for example, if your project has a `setup.py` like this:

..code-block:: python

    from setuptools import setup
    setup(
        name="calc",
        version="0.1",
        packages=['calc'],
        package_dir={'calc': 'calc'},
        install_requires=[
        'zope.interface',
        'requests',
        ],
        entry_points={
        'console_scripts': [
        'calc = calc.main:main',
        ]
        }
    )

Let’s check out what `pipit` has generated for us::
    
    $ tree target

    target/
    ├── bin
    │   ├── calc
    │   └── python
    ├── download
    │   └── zope.interface-4.2.0.tar.gz
    └── wheels
        ├── requests-2.10.0-py2.py3-none-any.whl
        ├── setuptools-25.1.1-py2.py3-none-any.whl
        └── zope.interface-4.2.0-cp27-cp27mu-macosx_10_11_x86_64.whl

Run your application::

    $ ./target/bin/calc
