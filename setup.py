from setuptools import setup, find_packages

setup(
    name='pydmtx',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy', 'pillow'],
    author='Grok 4 Heavy by xAI',
    description='Open-source Python library for Data Matrix ECC200 encoding/decoding from scratch',
    license='MIT',
    keywords='datamatrix barcode ecc200',
    url='https://github.com/xai-org/pydmtx',
)