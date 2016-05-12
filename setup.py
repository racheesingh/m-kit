from setuptools import setup, find_packages

setup(
    name="mkit",
    version='1.15',
    description="Internet Measurement Toolkit",
    author="Rachee Singh",
    author_email="racsingh@cs.stonybrook.edu",
    packages=find_packages(),
    install_requires=["py-radix"]
)

