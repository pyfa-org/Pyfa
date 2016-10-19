from pip.req import parse_requirements
from setuptools import setup, find_packages
# from eos import version
import config


parsed_reqs = parse_requirements('requirements.txt', session=False)
install_requires = [str(ir.req) for ir in parsed_reqs]


setup(
    name='Pyfa',
    description='Pyfa is a fitting program for for EVE Online.',
    version='{}'.format(config.version),
    author='Pyfa Team',
    author_email='',
    url='https://github.com/pyfa-org/Pyfa',
    packages=find_packages(exclude='tests'),
    install_requires=install_requires,
)
