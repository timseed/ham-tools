from setuptools import setup

setup(
    name='ham',
    version='1.0.2a',
    packages=['ham', 'ham.rbn', 'ham.adif', 'ham.band', 'ham.calc', 'ham.dxcc', 'ham.radio', 'ham.tests',
              'ham.beacon', 'ham.kpa500', 'ham.qsosvr', 'ham.telnet', 'ham.rotator'],
    url='',
    license='Public',
    author='tim',
    author_email='tim@sy-edm.com',
    description='Some Ham radio utils, which I use.',
    install_requires=['ephem', 'pyserial', 'pyyaml'],
)
