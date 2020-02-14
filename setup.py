from setuptools import setup

requirements = 'ephem', 'pyserial', 'pyyaml', 'geojson'

setup(
    name='ham',
    version='1.0.2b',
    packages=['ham', 'ham.rbn', 'ham.adif', 'ham.band', 'ham.calc', 'ham.dxcc',  'ham.tests',
              'ham.beacon',  'ham.qsosvr', 'ham.telnet', 'ham.equipment', 'ham.wsjx'],
    url='',
    license='Public',
    author='tim',
    author_email='tim@sy-edm.com',
    description='Some Ham radio utils, which I use.',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'sphinx',
            'recommonmark',
            'black',
            'pylint'
        ]},
    #Dev can be triggered by
    #python setup.py sdist
    #pip install dist/ham-1.0.2a0.tar.gz[dev]
    #
)

