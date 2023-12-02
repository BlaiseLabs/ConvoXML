from setuptools import setup, find_packages
from setuptools.dist import Distribution

# Define a custom Distribution class to read dependencies from requirements.txt
class MyDistribution(Distribution):
    def fetch_build_eggs(self, *args, **kwargs):
        if not self.install_requires:
            return []
        return super(MyDistribution, self).fetch_build_eggs(*args, **kwargs)

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='ConvoXML',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires,  # Read dependencies from requirements.txt
    url='https://github.com/BlaiseLabs/ConvoXML',
)
