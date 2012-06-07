from setuptools import setup, find_packages
from pip.req import parse_requirements
from os import path
here = path.abspath(path.dirname(__file__))

install_reqs = parse_requirements("./requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="bktree",
    version="0.0.1",
    install_requires=reqs,
    author="Jeethu Rao",
    author_email="jeethu@jeethurao.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bktree_demo = bktree.demo:main'
        ]
    }
)
