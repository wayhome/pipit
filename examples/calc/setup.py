from setuptools import setup
setup(
    name="calc",
    version="0.1",
    packages=['calc'],
    package_dir={'calc': 'calc'},
    install_requires=[
        'zope.interface',
        'zc.buildout==2.5.0',
        'tzone.client',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'calc_add = calc.main:add',
            'calc_mul = calc.main:mul',
        ]
    }
)
