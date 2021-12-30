from setuptools import setup, find_packages

setup(
    name='DECI',
    version='1.0',
    author='Chris Rae',
    author_email='raecd123@gmail.com',
    packages=find_packages(),
    install_requires=[
        "os",
        "socket",
        "random",
        "requests",
        "json",
        "python-magic-bin"
    ]
)
