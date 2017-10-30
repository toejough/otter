"""Setup for Otter."""


# [ Imports ]
from setuptools import setup, find_packages


# [ Script ]
setup(
    name='otter',
    version='0.1.1',
    description='Module to cleanly resume CLI output after an interruption on the CLI.',
    long_description=open('README.rst').read(),
    url='https://github.com/toejough/otter',
    author='toejough',
    author_email='toejough@gmail.com',
    license='MIT',
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            # Pick your license as you wish (should match "license" above)
             'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
    ],
    keywords="output cli",
    packages=find_packages(),
    install_requires=[],
)
