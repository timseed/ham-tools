from setuptools import setup, find_packages

requirements = 'wheel', 'ephem', 'pyserial', 'pyyaml', 'geojson','PyQt5'
for p in find_packages():
    print("Instaling ipackage "+str(p))
setup(
    name='ham',
    version='1.4.0',
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
            'pylint',
            'mock_pyserial'
        ]},
    #Dev can be triggered by
    #python setup.py sdist
    #pip install dist/ham-1.4.0.tar.gz[dev]
    #
)

