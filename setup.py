from setuptools import setup, find_packages

setup(
    name="squid",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'oandapyV20>=0.7.2',
        'pandas>=1.3.0',
        'pytz>=2021.1',
        'numpy>=1.19.0',
        'backoff>=1.10.0',
        'python-dotenv>=0.19.0'
    ],
)