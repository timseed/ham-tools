from setuptools import setup, find_packages

requirements = 'ephem', 'pyserial', 'pyyaml', 'geojson'

setup(
    name='ham',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True, #Uses Manifest.IN
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

